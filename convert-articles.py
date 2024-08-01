# coding: utf-8
import glob, os, re

def convert(text):
    title = text.split("\n")[0]
    content = "\n".join(text.split("\n")[1:])
    
    if title == "":
        return
    
    article = "<h2>" + title + "</h2>"

    for paragraph in content.split("\n"):
        article += "<p>" + paragraph + "</p>"

    return {
        "title": title,
        "content": content,
        "html": article
    }

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
            "<meta property=\"og:url\" content=\"https://raspython3.github.com/homepage/{}\" />").format(
                article["title"],
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
        article_list += "<div class=\"article-item\"><h2><a href=\"{}\">{}</a></h2><p>{}</p></div>".format(article[0], article[1]["title"], article[1]["content"].replace("\n", " ")[:100])

    with open("articles.html", mode="r+", encoding="utf-8") as f:
        html = f.read()

    with open("articles.html", mode="w+", encoding="utf-8") as f:
        f.write(re.sub("(?<=<!--articles start-->)(?:.|\\s)*(?=<!--articles end-->)", article_list, html))

if __name__ == "__main__":
    main()