import requests
from bs4 import BeautifulSoup
import os


class BlogSpider(object):

    def __init__(self):
        self.url = "http://www.yinwang.org/"
        self.session = requests.Session()

        self.urls = []

    def fetch_all_article_url(self):
        s = self.session
        res = s.get(self.url)
        # print res.text
        soup = BeautifulSoup(res.text, "lxml")

        # ul = soup.find_all("ul", class_="list-group")
        # print ul
        # for li in ul:
        #     print li
        ul = soup.select('ul.list-group li a')
        # print ul

        urls = []
        for li in ul:
            urls.append((li.string, li.get("href")))

        # print urls
        self.urls = urls
        return urls

        # res2 = s.get("http://yinwang.org/blog-cn/2016/08/29/microsoft")
        # print res2.text

    def fetch_each_article(self):
        s = self.session
        urls = self.urls

        articles = []
        count = 0
        length = len(urls)

        filenames = []
        # urls = [urls[-1]]
        for title, url in urls:
            res = s.get(url)

            soup = BeautifulSoup(res.text, "lxml")
            body = soup.body

            # articles.append((title, url, body))

            strs = u""
            stack = []
            children = []
            skip = []
            for child in body.descendants:
                # not None
                s_str = child.string

                # if child.name:
                #     if child.name == 'ol':
                #         # import pdb;pdb.set_trace()
                #         children.append(child.name)

                if child.name == 'p' and child.parent.name == 'li':
                    skip.append(child.name)
                    continue

                # todo: bug: when <p> in <li>, still have duplicated text
                if s_str:
                    if s_str not in stack:
                        stack.append(s_str)
                        strs += (s_str + "\n")
                    else:
                        stack.remove(s_str)

            # print skip, title
            # import pdb;pdb.set_trace()

            count += 1
            print "{} / {}".format(count, length)

            dir = "./blogs/"
            dir2 = "./blogs_html/"
            for d in {dir, dir2}:
                if not os.path.exists(d):
                    os.makedirs(d)

            filename = u"{}{} - {}.txt".format(dir, str(count).zfill(3), title)
            filename_html = u"{}{} - {}.html".format(dir2, str(count).zfill(3), title)

            if True:
                # pure text version
                f = open(filename, 'w')
                # "".join([item.string for item in body if item.string])
                f.write(strs.encode('utf8'))
                f.close()

                # html version

                f = open(filename_html, 'w')
                # "".join([item.string for item in body if item.string])
                f.write(res.text.encode('utf8'))
                f.close()

            filenames.append(filename_html)

        hrefs = []
        for name in filenames:
            # print name
            a_href = u"<li><a href='{name}'> {name} </a></li>".format(name=name)
            hrefs.append(a_href)

        menu = u"""
                <html>
                    <head>
                        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
                    </head>
                    <body>
                        <ul>
                            {}
                        </ul>

                    </body>
                </html>
                """.format("".join(hrefs))
        f = open('./index.html', 'w')
        f.write(menu.encode('utf8'))
        f.close()


        # print articles


bs = BlogSpider()
bs.fetch_all_article_url()
bs.fetch_each_article()



