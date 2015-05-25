package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"net/http"
	"os/exec"
	"runtime"
	"strings"
)

const (
	PocketAuthRequestURL = "https://getpocket.com/v3/oauth/request"
	PocketConfirmURL     = "https://getpocket.com/auth/authorize"
	PocketAuthorizeURL   = "https://getpocket.com/v3/oauth/authorize"
	PocketAddURL         = "https://getpocket.com/v3/add"
	PocketSendURL        = "https://getpocket.com/v3/send"
	RedirectURI          = "http://localhost:8889"
)

type PocketAPI struct {
	ConsumerKey  string
	RequestToken string
	AccessToken  string `json:"access_token"`
	Username     string `json:"username"`
}

type authParam struct {
	ConsumerKey string `json:"consumer_key,omitempty"`
	RedirectURI string `json:"redirect_uri,omitempty"`
}

type tokenParam struct {
	ConsumerKey string `json:"consumer_key"`
	AuthCode    string `json:"code"`
}

type pocketEntry struct {
	ConsumerKey string   `json:"consumer_key"`
	AccessToken string   `json:"access_token"`
	Actions     []action `json:"actinos"`
}

type action struct {
	URL   string `json:"url"`
	Title string `json:"title"`
	Tags  string `json:"tags"`
	Time  int64  `json:"time"`
}

func NewPocketAPI(key string) *PocketAPI {
	return &PocketAPI{
		ConsumerKey: key,
	}
}

func makeJSONPost(urlStr string, data []byte) (*http.Response, error) {
	req, err := http.NewRequest("POST", urlStr, bytes.NewBuffer(data))
	if err != nil {
		return nil, err
	}
	req.Header.Add("Content-Type", "application/json; charset=UTF-8")
	req.Header.Add("X-Accept", "application/json")
	return http.DefaultClient.Do(req)
}

// ObtainToken process Pocket's token acquiring procedure.
// Detailed flow is described in http://getpocket.com/developer/docs/authentication.
func (p *PocketAPI) ObtainToken() error {
	// Auth code retrieving.
	param := authParam{
		ConsumerKey: p.ConsumerKey,
		RedirectURI: RedirectURI,
	}
	body, err := json.Marshal(param)
	if err != nil {
		return fmt.Errorf("Code: Marshal: %v", err)
	}
	resp, err := makeJSONPost(PocketAuthRequestURL, body)
	if err != nil {
		return fmt.Errorf("Code: Post: %v", err)
	}
	data, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	// Request token retrieving.
	// 1. Starting callback handler
	// 2. Redirect user to authenticaiton page and confirm this app
	// 3. Fetch request token with gained auth code
	tparam := tokenParam{
		ConsumerKey: p.ConsumerKey,
	}
	err = json.Unmarshal(data, &tparam)
	if err != nil {
		return fmt.Errorf("Code: Unmarshal: %v --> %v\n%v", string(data), err, string(body))
	}

	doneCh, err := startWebServer()
	if err != nil {
		return fmt.Errorf("Code: error on starting callback: %v", err)
	}
	urlStr := PocketConfirmURL + "?request_token=" + tparam.AuthCode + "&redirect_uri=" + RedirectURI
	err = openURL(urlStr)
	if err != nil {
		return fmt.Errorf("Code: error on opening url: %v", err)
	}
	<-doneCh

	body, err = json.Marshal(tparam)
	if err != nil {
		return err
	}
	resp, err = makeJSONPost(PocketAuthorizeURL, body)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	data, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}
	err = json.Unmarshal(data, p)
	if err != nil {
		return fmt.Errorf("Token: Unmarshal: %v --> %v\n%v", string(data), err, string(body))
	}
	return nil
}

// MultiAdd is part of Modify method in Pocket API. The app has to have Modify access.
func (p *PocketAPI) MultiAdd(entries []Diigo) error {
	actions := make([]action, len(entries))
	for i, e := range entries {
		tags := strings.Join(e.Tags, ",")
		actions[i] = action{
			URL:   e.URL,
			Title: e.Title,
			Tags:  tags,
			Time:  e.Time,
		}
	}

	batch := len(entries)/100 + 1
	for i := 0; i < batch; i++ {
		log.Printf("sending %vth batch", i)
		var part []action
		if i == batch-1 {
			part = actions[i*100:]
		} else {
			part = actions[i*100 : (i+1)*100]
		}

		entry := pocketEntry{
			ConsumerKey: p.ConsumerKey,
			AccessToken: p.AccessToken,
			Actions:     part,
		}
		data, err := json.Marshal(entry)
		if err != nil {
			return err
		}
		_, err = makeJSONPost(PocketSendURL, data)
		if err != nil {
			return err
		}
	}
	return nil
}

// openURL launch the environment's default web browser with specified urlStr.
// Original code is:
//   http://stackoverflow.com/questions/10377243/how-can-i-launch-a-process-that-is-not-a-file-in-go
func openURL(urlStr string) error {
	var err error
	switch runtime.GOOS {
	case "linux":
		err = exec.Command("xdg-open", urlStr).Start()
	case "darwin":
		err = exec.Command("open", urlStr).Start()
	case "windows":
		err = exec.Command("rundll32", "url.dll.FileProtocolHandler", "http://localhost:4001/").Start()
	default:
		err = fmt.Errorf("Cannot open URL %s on this platform", urlStr)
	}
	return err
}

// startWebServer launches callback handler for authentication page of Pocket API.
func startWebServer() (chan bool, error) {
	listener, err := net.Listen("tcp", "localhost:8889")
	if err != nil {
		return nil, err
	}
	doneCh := make(chan bool)
	go http.Serve(listener, http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		doneCh <- true
		listener.Close()
		w.Header().Set("Content-Type", "text/plain")
		fmt.Fprintf(w, "Now you can close the browser safely.")
	}))
	return doneCh, nil
}
