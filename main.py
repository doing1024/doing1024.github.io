import sys
import os
import re
import shutil
import pypandoc
import fire
import toml


class Dlog:
    "dlog主逻辑类"

    def __init__(self):
        pass

    def __readconfig(self):
        return toml.load("config.toml")

    def __confirm(self, message, yes='y', no='n'):
        want_to_do = input(f"{message} [{yes}/{no}]:")
        while want_to_do not in (yes, no):
            want_to_do = input(f"please answer {yes} or {no}:")
        return bool(want_to_do == yes)

    def __newsite(self):
        if not self.__confirm(f"Do you want to create a new site at {os.getcwd()}?"):
            print("Abort!")
            sys.exit(1)
        os.mkdir("posts")
        os.mkdir("themes")
        with open("config.toml", "w"):
            pass

    def build(self, i=False):
        """实现dlog build命令"""
        config = self.__readconfig()
        if i:
            pypandoc.pandoc_download.download_pandoc()
        shutil.rmtree("build")
        os.mkdir("build")
        theme = config["theme"]
        for file in os.listdir("posts"):
            if os.path.isdir(file):
                continue
            postbody = pypandoc.convert_file(f"posts/{file}", "html")
            with open(f"build/{file.split('.')[0]}.html", "w") as output, open(f"themes/{theme}/template/post.html", "r") as tmplt:
                s = tmplt.read().replace("{{{postBody}}}", postbody)
                words = list(set(re.compile(r"\{\{\{.*\}\}\}").findall(s)))
                for word in words:
                    s = s.replace(word, config[word[3:-3]])
                output.write(s)

    def new(self, typ):
        """实现dlog new"""
        if typ == "site":
            self.__newsite()


if __name__ == "__main__":
    fire.Fire(Dlog)
