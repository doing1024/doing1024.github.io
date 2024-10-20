package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"sync"

	"github.com/BurntSushi/toml"
	"github.com/otiai10/copy"
)

type Config struct {
	SiteURL   string   `toml:"siteUrl"`
	SiteName  string   `toml:"siteName"`
	SiteTitle string   `toml:"siteTitle"`
	Theme     string   `toml:"theme"`
	NoBuildFiles []string `toml:"noBuildFiles"`
}

type Dlog struct {
	configPath string
	buildDir   string
	postsDir   string
	themesDir  string
	config     Config
}

func NewDlog() *Dlog {
	return &Dlog{
		configPath: getEnv("DLOG_CONFIG", "config.toml"),
		buildDir:   getEnv("DLOG_BUILD_DIR", "build"),
		postsDir:   getEnv("DLOG_POSTS_DIR", "posts"),
		themesDir:  getEnv("DLOG_THEMES_DIR", "themes"),
	}
}

func getEnv(key, fallback string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return fallback
}

func (d *Dlog) readConfig() error {
	_, err := toml.DecodeFile(d.configPath, &d.config)
	return err
}

func (d *Dlog) build() error {
	if err := d.readConfig(); err != nil {
		return fmt.Errorf("error reading config: %w", err)
	}

	if err := os.RemoveAll(d.buildDir); err != nil {
		return fmt.Errorf("error removing build directory: %w", err)
	}

	if err := os.MkdirAll(d.buildDir, 0755); err != nil {
		return fmt.Errorf("error creating build directory: %w", err)
	}

	for _, nobuildfile := range d.config.NoBuildFiles {
		src := filepath.Join(d.postsDir, nobuildfile)
		dst := filepath.Join(d.buildDir, nobuildfile)
		if err := copy.Copy(src, dst); err != nil {
			return fmt.Errorf("error copying no-build file %s: %w", nobuildfile, err)
		}
	}

	themeTemplateDir := filepath.Join(d.themesDir, d.config.Theme, "template")
	if err := d.copyAndReplaceThemeFiles(themeTemplateDir, d.buildDir); err != nil {
		return fmt.Errorf("error copying and replacing theme files: %w", err)
	}

	var wg sync.WaitGroup
	err := filepath.Walk(d.postsDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		relPath, err := filepath.Rel(d.postsDir, path)
		if err != nil {
			return err
		}

		for _, nobuildfile := range d.config.NoBuildFiles {
			if strings.HasPrefix(relPath, nobuildfile) {
				return nil
			}
		}

		if !info.IsDir() {
			wg.Add(1)
			go func(file string) {
				defer wg.Done()
				if err := d.buildFile(file); err != nil {
					log.Printf("Error building file %s: %v", file, err)
				}
			}(relPath)
		}

		return nil
	})

	wg.Wait()
	return err
}

func (d *Dlog) copyAndReplaceThemeFiles(src, dst string) error {
	return filepath.Walk(src, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		relPath, err := filepath.Rel(src, path)
		if err != nil {
			return err
		}

		dstPath := filepath.Join(dst, relPath)

		if info.IsDir() {
			return os.MkdirAll(dstPath, info.Mode())
		}

		content, err := ioutil.ReadFile(path)
		if err != nil {
			return err
		}

		replacedContent := d.replaceThemeVariables(string(content))

		return ioutil.WriteFile(dstPath, []byte(replacedContent), info.Mode())
	})
}

func (d *Dlog) replaceThemeVariables(content string) string {
	replacements := map[string]string{
		"{{{siteName}}}":  d.config.SiteName,
		"{{{siteUrl}}}":   d.config.SiteURL,
		"{{{siteTitle}}}": d.config.SiteTitle,
	}

	for old, new := range replacements {
		content = strings.ReplaceAll(content, old, new)
	}

	return content
}

func (d *Dlog) buildFile(file string) error {
	inputPath := filepath.Join(d.postsDir, file)
	outputPath := filepath.Join(d.buildDir, strings.TrimSuffix(file, filepath.Ext(file))+".html")

	if err := os.MkdirAll(filepath.Dir(outputPath), 0755); err != nil {
		return err
	}

	cmd := exec.Command("pandoc", "-f", "markdown", "-t", "html", inputPath, "-o", outputPath)
	if err := cmd.Run(); err != nil {
		return fmt.Errorf("pandoc conversion failed: %w", err)
	}

	content, err := ioutil.ReadFile(outputPath)
	if err != nil {
		return err
	}

	templatePath := filepath.Join(d.themesDir, d.config.Theme, "template", "post.html")
	template, err := ioutil.ReadFile(templatePath)
	if err != nil {
		return err
	}

	finalContent := strings.Replace(string(template), "{{{postBody}}}", string(content), 1)
	finalContent = d.replaceThemeVariables(finalContent)

	return ioutil.WriteFile(outputPath, []byte(finalContent), 0644)
}

func main() {
	dlog := NewDlog()
	if err := dlog.build(); err != nil {
		log.Fatalf("Build failed: %v", err)
	}
	log.Println("Build completed successfully.")
}
