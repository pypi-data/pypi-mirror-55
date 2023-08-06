"""
Wechat Media Platform crawler
"""
import os
import re
import logging
import pdfkit
import datetime
import base64
import urllib.parse as up
import hashlib


class cd:
    def __init__(self, path, create=False):
        self.lastwd = None
        self.path = path
        self.create = create

    def __enter__(self):
        if self.create:
            os.makedirs(self.path, exist_ok=True)
        self.lastwd = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.lastwd)

def dull(*args, **kwargs): pass

class Crawler(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import requests
        self.options = {
            "quiet": "",
            "disable-javascript": "",
        }
        self.session = requests.session()
        self.__mime__ = dict()

        if self.get("verbose"):
            self.logging = print
        else:
            self.logging = dull

    def embed_assets(self, soup):
        self.logging("[src]")
        # replacing [src]
        for node in soup.find_all(lambda node: node.attrs.get("src")):
            scheme, _, _, _, _, _ = up.urlparse(node.attrs.get("src"))
            if scheme == "data":
                continue
            asset_url = up.urljoin(self.get("url"), node.attrs.get("src"))
            self.logging("embeding {}".format(asset_url))

            response = self.session.get(asset_url)
            if response.status_code / 100 == 2:
                node["src"] = "data:{};base64,{}".format(response.headers.get("Content-Type"),
                                                         base64.b64encode(response.content).decode())

        self.logging("[data-src]")
        # [data-src]
        for node in soup.find_all(lambda node: node.attrs.get("data-src")):
            scheme, _, _, _, _, _ = up.urlparse(node.attrs.get("data-src"))
            if scheme == "data":
                continue
            asset_url = up.urljoin(self.get("url"), node.attrs.get("data-src"))
            self.logging("embeding {}".format(asset_url))

            response = self.session.get(asset_url)
            if response.status_code / 100 == 2:
                node["src"] = "data:{};base64,{}".format(response.headers.get("Content-Type"),
                                                         base64.b64encode(response.content).decode())

        self.logging("[style]")
        # [style]
        for node in soup.find_all(lambda node: node.attrs.get("style")):
            style: str = node.attrs.get("style")
            match = re.match('.*url\\((?P<url>.*)\\).*', style)
            if match:
                url = match.groupdict().get("url")
                scheme, _, _, _, _, _ = up.urlparse(url)
                if scheme == "data":
                    continue
                asset_url = up.urljoin(self.get("url"), url)
                self.logging("  embeding {}".format(asset_url))
                response = self.session.get(asset_url)
                if response.status_code / 100 == 2:
                    style = style.replace(url, "data:{};base64,{}".format(response.headers.get("Content-Type"),
                                                                          base64.b64encode(response.content).decode()))
                node["style"] = style

        self.logging("link[rel=stylesheet]")
        # link[rel=stylesheet]
        for node in soup.find_all("link", attrs={"rel": "stylesheet"}):
            asset_url = up.urljoin(self.get("url"), node.attrs.get("href"))
            self.logging("embeding {}".format(asset_url))

            response = self.session.get(asset_url)
            if response.status_code / 100 == 2:
                node["href"] = "data:{};base64,{}".format(response.headers.get("Content-Type"),
                                                          base64.b64encode(response.content).decode())

        title = self.get("title")
        title = re.sub("[|/+=]", "-", title)

        pdffilename = self.get("output") or (title + ".pdf")
        pdfkit.from_string(str(soup), pdffilename, options=self.options)

        if self.get("html"):
            htmlfilepath = self.get("html_output") or (title + ".html")
            htmlcontent = str(soup).replace("//res.wx.qq.com", "https://res.wx.qq.com").replace("https:https://res.wx.qq.com", "https://res.wx.qq.com")
            htmlcontent = htmlcontent.replace("//mp.weixin.qq.com", "https://mp.weixin.qq.com").replace("https:https://mp.weixin.qq.com", "https://mp.weixin.qq.com")
            with open(htmlfilepath, "w+") as fp:
                fp.write(htmlcontent)

    def save_assets_to_file(self, soup):
        os.makedirs("{}.assets".format(self.get("title")), exist_ok=True)

        self.logging("[src]")
        # replacing [src]
        for node in soup.find_all(lambda node: node.attrs.get("src")):
            scheme, _, _, _, _, _ = up.urlparse(node.attrs.get("src"))
            if scheme == "data":
                continue
            asset_url = up.urljoin(self.get("url"), node.attrs.get("src"))
            self.logging("saving {}".format(asset_url))

            response = self.session.get(asset_url)
            if response.status_code / 100 == 2:
                try:
                    filepath = "{}.assets/{}.{}".format(self.get("title"), hashlib.sha224(response.content).hexdigest(),
                                                        self.mime.get(response.headers.get("Content-Type", "data")))
                    with open(filepath, "wb+") as fp:
                        fp.write(response.content)
                    node["src"] = filepath
                except Exception as e:
                    self.logging(e)

        self.logging("[data-src]")
        # [data-src]
        for node in soup.find_all(lambda node: node.attrs.get("data-src")):
            scheme, _, _, _, _, _ = up.urlparse(node.attrs.get("data-src"))
            if scheme == "data":
                continue
            asset_url = up.urljoin(self.get("url"), node.attrs.get("data-src"))
            self.logging("saving {}".format(asset_url))

            response = self.session.get(asset_url)
            if response.status_code / 100 == 2:
                try:
                    filepath = "{}.assets/{}.{}".format(self.get("title"), hashlib.sha224(response.content).hexdigest(),
                                                        self.mime.get(response.headers.get("Content-Type", "data")))
                    with open(filepath, "wb+") as fp:
                        fp.write(response.content)
                    node["src"] = filepath
                except Exception as e:
                    self.logging(e)

        self.logging("[style]")
        # [style]
        for node in soup.find_all(lambda node: node.attrs.get("style")):
            style: str = node.attrs.get("style")
            match = (re.findall('url\\((?P<url>[^"()]+)\\)', style) or []) + (re.findall('url\\("(?P<url>[^"()]+)"\\)', style) or [])

            if match:
                self.logging(match, style)
                for url in match:
                    scheme, _, _, _, _, _ = up.urlparse(url)
                    if scheme == "data":
                        continue
                    asset_url = up.urljoin(self.get("url"), url)
                    self.logging("saving {}".format(asset_url))
                    response = self.session.get(asset_url)
                    if response.status_code / 100 == 2:
                        try:
                            filepath = "{}.assets/{}.{}".format(self.get("title"),
                                                                hashlib.sha224(response.content).hexdigest(),
                                                                self.mime.get(
                                                                    response.headers.get("Content-Type", "data")))
                            with open(filepath, "wb+") as fp:
                                fp.write(response.content)
                            style = style.replace(url, filepath)
                        except Exception as e:
                            self.logging(e)
                node["style"] = style

        self.logging("link[rel=stylesheet]")
        # link[rel=stylesheet]
        for node in soup.find_all("link", attrs={"rel": "stylesheet"}):
            asset_url = up.urljoin(self.get("url"), node.attrs.get("href"))
            self.logging("saving {}".format(asset_url))

            response = self.session.get(asset_url)
            if response.status_code / 100 == 2:
                try:
                    filepath = "{}.assets/{}.{}".format(self.get("title"),
                                                        hashlib.sha224(response.content).hexdigest(),
                                                        self.mime.get(response.headers.get("Content-Type", "data")))
                    with open(filepath, "wb+") as fp:
                        fp.write(response.content)
                    node["href"] = filepath
                except Exception as e:
                    self.logging(e)

        title = self.get("title")
        title = re.sub("[|/+=]", "-", title)

        htmlfilepath = self.get("html_output") or (title + ".html")
        htmlcontent = str(soup).replace("//res.wx.qq.com", "https://res.wx.qq.com")
        htmlcontent = htmlcontent.replace("//mp.weixin.qq.com", "https://mp.weixin.qq.com")
        htmlcontent = htmlcontent.replace("https:https:", "https:").replace("http:https:", "http:")
        with open(htmlfilepath, "w+") as fp:
            fp.write(htmlcontent)

        pdffilename = self.get("output") or (title + ".pdf")
        pdfkit.from_file(htmlfilepath, pdffilename, options=self.options)

    def save_webpage(self):
        import bs4

        try:
            htmlresponse = self.session.get(self.get("url"))
            soup = bs4.BeautifulSoup(htmlresponse.text, features='html.parser')

            # guess title and fallback to datetime
            title = datetime.datetime.now().strftime("%c")

            titlenode = soup.find("title")
            activitynode = soup.find(id="activity-name")
            ogtitlenode = soup.find(attrs={"property": "og:title"})
            twittertitlenode = soup.find(attrs={"property": "twitter:title"})

            self.logging("searching for title...")
            self.logging("    title:                    {}".format((titlenode.text if titlenode else "").strip()))
            self.logging("    #activity-name:           {}".format((activitynode.text if activitynode else "").strip()))
            self.logging("    [property=og:title]:      {}".format(
                (ogtitlenode.attrs.get("content").strip() if ogtitlenode else "").strip()))
            self.logging("    [property=twitter:title]: {}".format(
                (twittertitlenode.attrs.get("content").strip() if twittertitlenode else "").strip()))
            if soup.find("title") is not None and soup.find("title").text.strip():
                title = soup.find("title").text.strip()
            elif activitynode is not None and activitynode.text.strip():
                title = activitynode.text.strip()
            elif ogtitlenode is not None and ogtitlenode.attrs.get("content").strip():
                title = ogtitlenode.attrs.get("content").strip()
            elif twittertitlenode is not None and twittertitlenode.attrs.get("content").strip():
                title = twittertitlenode.attrs.get("content").strip()
            else:
                self.logging("")
            self.update({
                "title": title
            })

            getattr(self, self.get("method"))(soup)

        except:
            raise

    @property
    def mime(self):
        if not len(self.__mime__.keys()):
            with open("/etc/mime.types") as fp:
                for line in fp:
                    line = line.strip()
                    if not line.split("#")[0]:
                        continue
                    line = re.split("[\t ]+", line)
                    if len(line) < 2:
                        continue
                    mimetype, exts = line[0], line[1]
                    self.__mime__.update({
                        mimetype: exts.split(" ")[0]
                    })
        return self.__mime__

    def do(self):
        os.chdir(self.get("chdir"))
        self.save_webpage()

    @staticmethod
    def args():
        import argparse
        import sys
        parser = argparse.ArgumentParser(sys.argv[0])

        parser.add_argument("url", help="url to save")
        parser.add_argument("--method", choices=["embed_assets", "save_assets_to_file"], default="save_assets_to_file")

        parser.add_argument("--output", help="pdf path for saving")
        parser.add_argument("--html", default=False, action="store_true", help="save unified html content")
        parser.add_argument("--html-output", help="html path for saving")
        parser.add_argument("--verbose", "-v", default=False, action="store_true")

        parser.add_argument("--chdir", default=".")

        return parser.parse_args()


if __name__ == "__main__":
    Crawler(**vars(Crawler.args())).do()
