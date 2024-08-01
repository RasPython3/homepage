# coding: utf-8
import glob, os, re

def convert(text):
    title = text.split("\n")[0]
    content = decorate("\n".join(text.split("\n")[1:]))
    
    if title == "":
        return
    
    article = "<h2>" + title + "</h2>" + content

    return {
        "title": title,
        "content": content,
        "description": re.sub("(?:<[^>]*>)", "", content)[:100].replace("\n", " "),
        "html": article
    }

def decorate(text):
    result = re.sub("((?:> )?)(.+)", "\\1<p>\\2</p>", text)
    result = re.sub("(?:(?<=\n)> [^\n]*\n)+", lambda m: "<div class=\"quoted\">" + re.sub("(?:^|(?<=\n))> ", "", m[0]) + "</div>", result)

    lines = []

    for line in result.split("\n"):
        index = 0
        flags={"i": 0, "b": 0, "code": 0}
        level=0

        temps = [""]

        decoration_length = 0

        while len(line) > index:
            if line[index:index+2] == "**":
                if flags["b"] > 0:
                    if flags["b"] <= level and (decoration_length > 0 or flags["b"] < level):
                        if flags["i"] > flags["b"]:
                            temps[flags["i"]] = "*" + temps[flags["i"]]
                            flags["i"] = 0
                        if flags["code"] > flags["b"]:
                            temps[flags["code"]] = "`" + temps[flags["code"]]
                            flags["code"] = 0
                        level = flags["b"] - 1
                        flags["b"] = 0
                        temps[level] += "<b>" + "".join(temps[level+1:])  + "</b>"
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
                        if flags["code"] > flags["b"]:
                            temps[flags["code"]] = "`" + temps[flags["code"]]
                            flags["code"] = 0
                        level = flags["i"] - 1
                        flags["i"] = 0
                        temps[level] += "<i>" + "".join(temps[level+1:])  + "</i>"
                        temps = temps[:level+1]
                    else:
                        temps[-1] += "*"
                else:
                    decoration_length = 0
                    level += 1
                    flags["i"] = level
                    temps.append("")
                index += 1
            elif line[index] == "`":
                if flags["code"] > 0:
                    if flags["code"] <= level and (decoration_length > 0 or flags["code"] < level):
                        if flags["b"] > flags["code"]:
                            temps[flags["b"]] = "**" + temps[flags["b"]]
                            flags["b"] = 0
                        if flags["i"] > flags["code"]:
                            temps[flags["i"]] = "*" + temps[flags["i"]]
                            flags["i"] = 0
                        level = flags["code"] - 1
                        flags["code"] = 0
                        temps[level] += "<span class=\"code\">" + "".join(temps[level+1:])  + "</span>"
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

        if level > 0:
            if flags["b"] > 0:
                temps[flags["b"]] = "**" + temps[flags["b"]]
            if flags["i"] > 0:
                temps[flags["i"]] = "*" + temps[flags["i"]]
            if flags["code"] > 0:
                temps[flags["code"]] = "`" + temps[flags["code"]]
            temps = ["".join(temps)]

        lines.append(temps[0])

    def tag_handler(m):
        tag, value = m.groups()
        if tag == "img":
            return "<img src=\"{}\">".format(value)
        return m[0]

    result = ""

    for line in lines:
        result += re.sub("^(?:<[^>]*>)*(?P<tag>[a-z]+):[ ]*(?P<value>[^<>]*)(?:<[^>]*>)*$", tag_handler, line) + "\n"

    return result

def main():
    articles = []
    with open("article-template.html", mode="r") as f:
        template = f.read()

    for fname in glob.glob("articles/sources/*.txt"):
        m = re.match("(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2})\\.txt", fname.replace("\\", "/").split("/")[-1])
        if m == None:
            print("invalid file name")
            continue

        with open(fname, mode="r", encoding="utf-8") as f:
            source = f.read()

        article = convert(source)

        if article == None:
            print("invalid article")
            continue

        page = template.replace("<!--article-->", article["html"])

        path = "articles/{:04}{:02}{:02}/".format(
            int(m.groups()[0]),
            int(m.groups()[1]),
            int(m.groups()[2])
        )

        page = page.replace("<!--open graph-->",
            ("<meta property=\"og:title\" content=\"{} / RasPython's Room\" />" + \
            "<meta property=\"og:description\" content=\"{}\" />" + \
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

        articles.append((path, article))

    article_list = ""

    for article in articles:
        article_list += "<div class=\"article-item\"><h2><a href=\"{}\">{}</a></h2><p>{}</p></div>".format(article[0], article[1]["title"], article[1]["description"])

    with open("articles.html", mode="r+", encoding="utf-8") as f:
        html = f.read()

    with open("articles.html", mode="w+", encoding="utf-8") as f:
        f.write(re.sub("(?<=<!--articles start-->)(?:.|\\s)*(?=<!--articles end-->)", article_list, html))

if __name__ == "__main__":
    main()