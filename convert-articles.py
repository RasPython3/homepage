# coding: utf-8
import glob, os, re

def convert(text, date="投稿日時不明"):
    title = text.split("\n")[0]
    content = decorate("\n".join(text.split("\n")[1:]))

    if title == "":
        return

    article = "<div class=\"article-header\"><h2>" + title + "</h2>" + "<span class=\"date\">" + date + "</span></div>" + content

    return {
        "title": title,
        "content": content,
        "description": re.sub("(?:<[^>]*>)", "", content)[:100].replace("\n", " "),
        "html": article
    }

def decorate(text):
    result = re.sub("(?:(?<=\n)> [^\n]*\n)+", lambda m: "<div class=\"quoted\">" + re.sub("(?:^|(?<=\n))> ", "", m[0]) + "</div>", text)

    lines = []

    flags = {"i": 0, "b": 0, "s": 0, "code": 0, "quoted": 0, "codeblock": 0}
    temps = [""]
    level=0
    decoration_length = 0

    overlined = 0

    for line in result.split("\n"):
        index = 0
        line_length = len(line)

        while line_length > index:
            if line_length >= index+3 and line[index:index+3] == "```":
                if flags["codeblock"] > 0:
                    if flags["codeblock"] <= level and (decoration_length > 0 or flags["codeblock"] < level):
                        level = flags["codeblock"] - 1
                        flags["codeblock"] = 0
                        lang = temps[level+1].split("\n")[0]
                        if lang == "":
                            lang = "text"
                        temps[level] += "<pre class=\"codeblock lang-{}\"><code>".format(lang) + re.sub("(?:^[a-zA-Z]*\n+)|(?:\n+$)", "", "".join(temps[level+1:])).replace("\n", "</code>\n<code>")  + "</code></pre>"
                        if line_length > index + 3:
                            temps[level] += "\n"
                        temps = temps[:level+1]
                    else:
                        temps[-1] += "```"
                else:
                    decoration_length = 0
                    level += 1
                    flags["codeblock"] = level
                    if index > 0:
                        temps[-1] += "\n"
                    temps.append("")
                index += 3
            elif flags["codeblock"] == 0:
                if line[index:index+2] == "**":
                    if flags["b"] > 0:
                        if flags["b"] <= level and (decoration_length > 0 or flags["b"] < level):
                            if flags["i"] > flags["b"]:
                                temps[flags["i"]] = "*" + temps[flags["i"]]
                                flags["i"] = 0
                            if flags["s"] > flags["b"]:
                                temps[flags["s"]] = "~~" + temps[flags["s"]]
                                flags["s"] = 0
                            if flags["code"] > flags["b"]:
                                temps[flags["code"]] = "`" + temps[flags["code"]]
                                flags["code"] = 0
                            level = flags["b"] - 1
                            flags["b"] = 0
                            temps[level] += "<b>" + "".join(temps[level+1:]).replace("\n", "</b>\n<b>")  + "</b>"
                            temps = temps[:level+1]
                        else:
                            temps[-1] += "**"
                    else:
                        decoration_length = 0
                        level += 1
                        flags["b"] = level
                        temps.append("")
                    index += 2
                elif line[index] == "*":
                    if flags["i"] > 0:
                        if flags["i"] <= level and (decoration_length > 0 or flags["i"] < level):
                            if flags["b"] > flags["i"]:
                                temps[flags["b"]] = "**" + temps[flags["b"]]
                                flags["b"] = 0
                            if flags["s"] > flags["i"]:
                                temps[flags["s"]] = "~~" + temps[flags["s"]]
                                flags["s"] = 0
                            if flags["code"] > flags["b"]:
                                temps[flags["code"]] = "`" + temps[flags["code"]]
                                flags["code"] = 0
                            level = flags["i"] - 1
                            flags["i"] = 0
                            temps[level] += "<i>" + "".join(temps[level+1:]).replace("\n", "</i>\n<i>")  + "</i>"
                            temps = temps[:level+1]
                        else:
                            temps[-1] += "*"
                    else:
                        decoration_length = 0
                        level += 1
                        flags["i"] = level
                        temps.append("")
                    index += 1
                elif line[index:index+2] == "~~":
                    if flags["s"] > 0:
                        if flags["s"] <= level and (decoration_length > 0 or flags["s"] < level):
                            if flags["b"] > flags["s"]:
                                temps[flags["b"]] = "**" + temps[flags["b"]]
                                flags["b"] = 0
                            if flags["i"] > flags["s"]:
                                temps[flags["i"]] = "*" + temps[flags["i"]]
                                flags["i"] = 0
                            if flags["code"] > flags["s"]:
                                temps[flags["code"]] = "`" + temps[flags["code"]]
                                flags["code"] = 0
                            level = flags["s"] - 1
                            flags["s"] = 0
                            temps[level] += "<s>" + "".join(temps[level+1:]).replace("\n", "</s>\n<s>")  + "</s>"
                            temps = temps[:level+1]
                        else:
                            temps[-1] += "~~"
                    else:
                        decoration_length = 0
                        level += 1
                        flags["s"] = level
                        temps.append("")
                    index += 2
                elif line[index] == "`":
                    if flags["code"] > 0:
                        if flags["code"] <= level and (decoration_length > 0 or flags["code"] < level):
                            if flags["b"] > flags["code"]:
                                temps[flags["b"]] = "**" + temps[flags["b"]]
                                flags["b"] = 0
                            if flags["i"] > flags["code"]:
                                temps[flags["i"]] = "*" + temps[flags["i"]]
                                flags["i"] = 0
                            if flags["s"] > flags["code"]:
                                temps[flags["s"]] = "~~" + temps[flags["s"]]
                                flags["s"] = 0
                            level = flags["code"] - 1
                            flags["code"] = 0
                            temps[level] += "<span class=\"code code-start"
                            codes = "".join(temps[level+1:]).split("\n")
                            for code in codes[:-1]:
                                temps[level] += "\">" + code + "</span>\n<span class=\"code"
                            temps[level] += " code-end\">" + codes[-1] + "</span>"
                            temps = temps[:level+1]
                        else:
                            temps[-1] += "`"
                    else:
                        decoration_length = 0
                        level += 1
                        flags["code"] = level
                        temps.append("")
                    index += 1
                else:
                    temps[-1] += line[index]
                    decoration_length += 1
                    index += 1
            else:
                temps[-1] += line[index]
                decoration_length += 1
                index += 1

        if level == 0:
            lines.extend(temps[0].split("\n"))
            temps = [""]
            overlined = 0
        else:
            temps[-1] += "\n"
            overlined = level

    if level > 0:
        if flags["b"] > 0:
            temps[flags["b"]] = "**" + temps[flags["b"]]
        if flags["i"] > 0:
            temps[flags["i"]] = "*" + temps[flags["i"]]
        if flags["s"] > 0:
            temps[flags["s"]] = "~~" + temps[flags["s"]]
        if flags["code"] > 0:
            temps[flags["code"]] = "`" + temps[flags["code"]]
        if flags["codeblock"] > 0:
            temps[flags["codeblock"]] = "```" + temps[flags["codeblock"]]
        temps = ["".join(temps)]
        lines.extend(temps[0].split("\n"))

    def tag_handler(m):
        tag, value = m.groups()
        if tag == "img":
            return "<img src=\"{}\">".format(value)
        elif tag == "file":
            if value != "":
                return "<a href=\"{}\" download>{}</a>".format(value, re.match("^(?:.*[/\\\\])?([^/\\\\]+)$", value).groups()[0])
        elif tag == "code":
            if value != "":
                lang = re.match("^.*?((?<=\\.)[a-zA-Z]*)$", value).groups()[0]
                if lang == "":
                    lang = "text"
                return "<pre class=\"codeblock lang-{}\"><code>{}</code></pre>".format(lang, value)
        return m[0]

    result = ""

    for line in lines:
        result += re.sub("^(?:<[^>]*>)*(?P<tag>[a-z]+):[ ]*(?P<value>[^<>]*)(?:<[^>]*>)*$", tag_handler, line) + "\n"

    result = re.sub("(^|\n)(?!<(?:pre|code)[ >])((?:> )?)(.*)", "\\1\\2<p>\\3</p>", result).replace("<p></p>", "<br>")

    return result

def main():
    with open("article-template.html", mode="r") as f:
        template = f.read()

    article_list = ""

    for fname in reversed(sorted(glob.glob("articles/sources/*.txt"))):
        m = re.match("(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2})-(?P<hour>\\d{2})(?P<minute>\\d{2})\\.txt", fname.replace("\\", "/").split("/")[-1])
        if m == None:
            print("invalid file name")
            continue

        with open(fname, mode="r", encoding="utf-8") as f:
            source = f.read()

        date_str = "{}-{:02}-{:02} {:02}:{:02}".format(
            int(m.groups()[0]),
            int(m.groups()[1]),
            int(m.groups()[2]),
            int(m.groups()[3]),
            int(m.groups()[4])
        )

        article = convert(source, date=date_str)

        if article == None:
            print("invalid article")
            continue

        page = template.replace("<!--article-->", article["html"])

        path = "articles/{:04}{:02}{:02}{:02}{:02}/".format(
            int(m.groups()[0]),
            int(m.groups()[1]),
            int(m.groups()[2]),
            int(m.groups()[3]),
            int(m.groups()[4])
        )

        page = page.replace("<!--open graph-->",
            ("<meta property=\"og:title\" content=\"{} / RasPython3's Room\" />" + \
            "<meta property=\"og:description\" content=\"{}...\" />" + \
            "<meta property=\"og:url\" content=\"https://raspython3.github.com/homepage/{}\" />").format(
                article["title"],
                article["description"],
                path)
        )

        try:
            os.mkdir(path[:-1])
        except:
            pass

        with open(path + "index.html", mode="w", encoding="utf-8") as f:
            f.write(page)

        article_list += "<div class=\"article-item\"><h2><a href=\"{}\">{}</a></h2><span>{}</span><p>{}</p></div>".format(
            path,
            article["title"],
            date_str,
            article["description"]
        )
        
    with open("articles.html", mode="r+", encoding="utf-8") as f:
        html = f.read()

    with open("articles.html", mode="w+", encoding="utf-8") as f:
        f.write(re.sub("(?<=<!--articles start-->)(?:.|\\s)*(?=<!--articles end-->)", article_list, html))

if __name__ == "__main__":
    main()