import os
import threading
import re
import shutil
import pypandoc
import toml
import logging


class Dlog:
    "dlog主逻辑类"

    def __init__(self):
        self.config_path = os.environ.get("DLOG_CONFIG", "config.toml")
        self.build_dir = os.environ.get("DLOG_BUILD_DIR", "build")
        self.posts_dir = os.environ.get("DLOG_POSTS_DIR", "posts")
        self.themes_dir = os.environ.get("DLOG_THEMES_DIR", "themes")

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def __readconfig(self):
        try:
            return toml.load(self.config_path)
        except toml.TomlDecodeError as e:
            self.logger.error(f"Error reading config file: {e}")
            raise

    def __build(self, file, config, theme):
        try:
            postbody = pypandoc.convert_file(os.path.join(self.posts_dir, file), "html")
            output_file = os.path.join(
                self.build_dir, f"{os.path.splitext(file)[0]}.html"
            )
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            with open(output_file, "w") as output, open(
                os.path.join(self.themes_dir, theme, "template", "post.html"), "r"
            ) as tmplt:
                s = (
                    tmplt.read()
                    .replace("{{{postBody}}}", postbody)
                    .replace("file:///", config["siteUrl"])
                )
                words = list(set(re.compile(r"\{\{\{.*\}\}\}").findall(s)))
                for word in words:
                    s = s.replace(word, config[word[3:-3]])
                output.write(s)
        except Exception as e:
            self.logger.error(f"Error building file {file}: {e}")

    def build(self):
        """实现dlog build命令"""
        try:
            config = self.__readconfig()

            if os.path.exists(self.build_dir):
                self.logger.info(f"Removing existing build directory: {self.build_dir}")
                shutil.rmtree(self.build_dir)

            os.mkdir(self.build_dir)

            theme = config["theme"]

            for nobuildfile in config["noBuildFiles"]:
                src = os.path.join(self.posts_dir, nobuildfile)
                dst = os.path.join(self.build_dir, nobuildfile)
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

            theme_template_dir = os.path.join(self.themes_dir, theme, "template")
            for item in os.listdir(theme_template_dir):
                src = os.path.join(theme_template_dir, item)
                dst = os.path.join(self.build_dir, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

            threads = []
            for root, _, files in os.walk(self.posts_dir):
                for file in files:
                    file_path = os.path.relpath(
                        os.path.join(root, file), self.posts_dir
                    )
                    if not any(
                        file_path.startswith(nobuildfile)
                        for nobuildfile in config["noBuildFiles"]
                    ):
                        thread = threading.Thread(
                            target=self.__build, args=(file_path, config, theme)
                        )
                        threads.append(thread)
                        thread.start()

            for thread in threads:
                thread.join()

            self.logger.info("Build completed successfully.")
        except Exception as e:
            self.logger.error(f"Build failed: {e}")


if __name__ == "__main__":
    dlog = Dlog()
    dlog.build()
