import os  # 操作文件
import threading  # 多线程
import re  # 正则表达式
import shutil  # 操作文件plus
import pypandoc  # pandoc的python封装
import toml  # 读取配置文件


class Dlog:
    "dlog主逻辑类"

    # 读取config.toml文件
    def __readconfig(self):
        return toml.load("config.toml")

    # build一个文件
    def __build(
        self, file, config, theme
    ):  # file为要部署的文件，config为配置读取的字典，theme为配置中的主题
        postbody = pypandoc.convert_file(f"posts/{file}", "html")
        try:  # 尝试新建文件
            os.makedirs(os.path.dirname(os.path.join("build", file)))
        except:  # 如果文件存在，则不新建
            pass
        with open(f"build/{file.split('.')[0]}.html", "w") as output, open(
            f"themes/{theme}/template/post.html", "r"
        ) as tmplt:  # 写入目标文件，读取主题文件
            s = (
                tmplt.read()
                .replace("{{{postBody}}}", postbody)  # 替换文章内容
                .replace("file:///", config["siteUrl"])  # 替换Linux的特别情况
            )
            words = list(
                set(re.compile(r"\{\{\{.*\}\}\}").findall(s))
            )  # 查找需要在配置文件寻找的值
            for word in words:
                s = s.replace(word, config[word[3:-3]])  # 逐一替换
            output.write(s)  # 写入

    def build(self):
        """实现dlog build命令"""
        config = self.__readconfig()  # 读取配置
        try:
            shutil.rmtree("build")  # 删除上次生成的文件
        except:
            pass
        os.mkdir("build")  # 新建文件夹
        theme = config["theme"]  # 读取主题
        for nobuildfile in config["noBuildFiles"]:  # 拷贝无需转化的文件
            try:  # 文件夹
                shutil.copytree(f"posts/{nobuildfile}", f"./build/{nobuildfile}")
            except:  # 文件
                shutil.copy(f"posts/{nobuildfile}", f"build/{nobuildfile}")
        for file in os.listdir(f"themes/{theme}/template/"):  # 将主题文件逐一拷贝
            try:  # 文件夹
                shutil.copytree(
                    os.path.join(f"themes/{theme}/template/", file), "build/"
                )
            except:  # 文件
                shutil.copy(os.path.join(f"themes/{theme}/template/", file), "build/")
        for file1, _, file2 in os.walk("posts"):  # 遍历文章
            for file3 in file2:
                file = os.path.join(file1, file3)
                file = re.sub(".*posts/", "", file)
                flag = False
                for nobuildfile in config["noBuildFiles"]:
                    if file.startswith(nobuildfile):
                        flag = True
                        break
                if not flag:
                    threading.Thread(
                        target=self.__build, args=(file, config, theme)
                    ).start()


if __name__ == "__main__":
    dlog = Dlog()
    dlog.build()
