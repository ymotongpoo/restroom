// This program renames filename of recorded mp3 or aac of 伊集院光 深夜の馬鹿力.
// Target files should be named in format of "yyyymmdd-NNN.(mp3|m4a)" and
// will be renamed to "伊集院光 深夜の馬鹿力 yyyy年mm月dd日 第NNN回.(mp3|m4a)".
package main

import (
	"flag"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"
)

var (
	src = flag.String("src", "", "directory where mp3 or aac files are")
)

func main() {
	flag.Parse()

	srcDir, err := os.Open(*src)
	if os.IsNotExist(err) {
		log.Fatalf("Directory '%v' does not exist: %v", *src, err)
	}

	files, err := srcDir.Readdir(-1)
	if err != nil {
		log.Fatalf("Error occured on reading '%v': %v", *src, err)
	}

	for _, f := range files {
		var ext string
		switch {
		case strings.HasSuffix(f.Name(), ".mp3"):
			ext = ".mp3"
		case strings.HasSuffix(f.Name(), ".m4a"):
			ext = ".m4a"
		default:
			continue
		}

		index := strings.LastIndex(f.Name(), ".")
		base := f.Name()[0:index]
		oldpath := filepath.Join(*src, f.Name())

		// file base name should be "YYYYmmdd-NNN"
		matched, err := regexp.MatchString(`\d{8}\-\d{3,4}`, base)
		if err != nil || !matched {
			continue
		}

		elements := strings.Split(base, "-")
		dateStr := elements[0]
		numberStr := elements[1]

		time, err := time.Parse("20060102", dateStr)
		if err != nil {
			log.Printf("Error occured to read date '%v': %v", dateStr, err)
			continue
		}
		filename := time.Format("伊集院光 深夜の馬鹿力 2006年01月02日") + " 第" + numberStr + "回" + ext
		newpath := filepath.Join(*src, filename)
		if err := os.Rename(oldpath, newpath); err != nil {
			log.Printf("Error on renaming '%v' -> '%v'", oldpath, newpath)
		}
	}
}
