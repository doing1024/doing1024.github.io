import sys
import os
import re
import shutil
import pypandoc
import fire
import toml
import threading

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
        print("If you want to get a example theme,please go to ")
        
    def __build(self, file, config, theme):
        postbody = pypandoc.convert_file(f"posts/{file}", "html")
        try:
            os.makedirs(os.path.dirname(os.path.join("build",file)))
        except:
            pass
        with open(f"build/{file.split('.')[0]}.html", "w") as output, open(f"themes/{theme}/template/post.html", "r") as tmplt:
            s = tmplt.read().replace("{{{postBody}}}", postbody).replace(
                "file:///", config["siteUrl"])
            words = list(set(re.compile(r"\{\{\{.*\}\}\}").findall(s)))
            for word in words:
                s = s.replace(word, config[word[3:-3]])
            output.write(s)

    def build(self):
        """实现dlog build命令"""
        config = self.__readconfig()
        shutil.rmtree("build")
        os.mkdir("build")
        theme = config["theme"]
        for nobuildfile in config["noBuildFiles"]:
            try:
                shutil.copytree(f"posts/{nobuildfile}", f"./build/{nobuildfile}")
            except:
                pass
        for file in os.listdir(f"themes/{theme}/template/"):
            shutil.copy(os.path.join(f"themes/{theme}/template/",file),"build/")
        for file1,_,file2 in os.walk("posts"):
            for file3 in file2:
                file = os.path.join(file1,file3)
                file  = re.sub(".*posts/","",file)
                flag = False
                for nobuildfile in config["noBuildFiles"]:
                    if file.startswith(nobuildfile):
                        flag = True
                        break
                if not flag:
                    threading.Thread(target=self.__build, args=(
                        file, config, theme)).start()

    def new(self, typ):
        """实现dlog new"""
        if typ == "site":
            self.__newsite()


if __name__ == "__main__":
    fire.Fire(Dlog)
