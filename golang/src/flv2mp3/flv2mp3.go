package main

import (
	"flag"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

var (
	dst   = flag.String("dst", "", "target directory where converted files goes to.")
	src   = flag.String("src", "", "source directory where original files exist.")
	ijuin = flag.Bool("ijuin", false, "convert 伊集院光 file mode")
	acopy = flag.Bool("acopy", false, "use -acodec copy option on ffmpeg")
)

func main() {
	flag.Parse()

	srcDir, err := os.Open(*src)
	if os.IsNotExist(err) {
		log.Fatalf("Directory '%v' does not exist: %v", *src, err)
	}
	_, err = os.Open(*dst)
	if os.IsNotExist(err) {
		log.Fatalf("Directory '%v' does not exist: %v", *dst, err)
	}

	files, err := srcDir.Readdir(-1)
	if err != nil {
		log.Fatalf("Error occured on reading '%v': %v", *src, err)
	}

	for _, f := range files {
		if strings.HasSuffix(f.Name(), ".flv") {
			base := strings.TrimRight(f.Name(), ".flv")
			log.Printf("start converting '%v': %v bytes", f.Name(), f.Size())
			srcFile := filepath.Join(*src, f.Name())
			dstFile := filepath.Join(*dst, base+".mp3")

			cmd := newConvertCmd(srcFile, dstFile)
			err := cmd.Run()
			if err != nil {
				log.Printf("Error occured, skipped: %v", err)
				continue
			}
			log.Printf("finished converting '%v'", f.Name())
		}
	}
}

func newConvertCmd(srcFile, dstFile string) *exec.Cmd {
	var cmdStr []string
	if *acopy {
		cmdStr = []string{"ffmpeg", "-y", "-i", srcFile, "-vn", "-acodec", "copy", dstFile}
	} else {
		cmdStr = []string{"ffmpeg", "-y", "-i", srcFile, "-vn", "-acodec", "libmp3lame", "-ac", "2", "-ab", "32000", "-ar", "44100", "-threads", "4", "-strict", "experimental", dstFile}
	}
	cmd := exec.Command(cmdStr[0], cmdStr[1:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd
}
