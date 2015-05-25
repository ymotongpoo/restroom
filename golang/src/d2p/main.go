package main

import (
	"fmt"
	"io"
	"log"
	"os"
	"strconv"
	"strings"

	"gopkg.in/xmlpath.v2"
)

var (
	atag  = xmlpath.MustCompile("//dt/a")
	href  = xmlpath.MustCompile("./@href")
	tags  = xmlpath.MustCompile("./@tags")
	added = xmlpath.MustCompile("./@add_date")
)

// Diigo is a struct to hold each entries information extracted from
// delicious style bookmark export data.
// You can get one on https://www.diigo.com/tools/export, and check "Delicious Format".
type Diigo struct {
	URL   string
	Tags  []string
	Title string
	Time  int64
}

// ExtractEntries reads delicious formatted date from r, parses them and store in a slice of Diigo.
func ExtractEntries(r io.Reader) ([]Diigo, error) {
	root, err := xmlpath.ParseHTML(r)
	if err != nil {
		return nil, err
	}

	iter := atag.Iter(root)
	entries := []Diigo{}
	for iter.Next() {
		node := iter.Node()
		urlStr, _ := href.String(node)
		tagsStr, _ := tags.String(node)
		title := node.String()
		addTime, _ := added.String(node)
		addTimeInt, err := strconv.ParseInt(addTime, 0, 64)
		if err != nil {
			return nil, err
		}
		d := Diigo{
			URL:   urlStr,
			Tags:  strings.Split(tagsStr, ","),
			Title: title,
			Time:  addTimeInt,
		}
		entries = append(entries, d)
	}

	return entries, nil
}

func usage() {
	fmt.Printf("usage: %v filename\n", os.Args[0])
	fmt.Println("filename: filename of delicious style bookmark file in HTML.")
}

// ConsumerKey constant is provided from key_<platform>.go file, which is not
// tracked on VCS to avoid direct leak of this app's consumer key. If you build
// similar application based on this source code, you can create one in following style:
//
//   package main
//
//   const ConsumerKey = "xxxxxx-xxxxxxxxxxxxxx"<EOF>
//
// The case you need platform specific files (i.e. key_<platform>.go) is you run go build
// in several platforms or do cross compiling. In most cases you just need key.go.
//
// When you develop your own, you can acquire new consumer key on http://getpocket.com/developer/apps/.
func main() {
	// extract diigo entries from file
	if len(os.Args) < 2 {
		usage()
		return
	}
	filename := os.Args[1]
	log.Printf("importing file: %v", filename)
	file, err := os.Open(filename)
	if err != nil {
		log.Fatalf("%v", err)
	}
	defer file.Close()

	entries, err := ExtractEntries(file)
	if err != nil {
		log.Fatalf("%v", err)
	}

	// pocket authorization
	p := NewPocketAPI(ConsumerKey)
	err = p.ObtainToken()
	if err != nil {
		log.Fatalf("%v", err)
	}

	err = p.MultiAdd(entries)
	if err != nil {
		log.Fatalf("%v", err)
	}
}
