# coding:utf-8
import requests
from bs4 import BeautifulSoup
import re
from requests.adapters import HTTPAdapter

"""
url = https://docs.docker.com/docker-trusted-registry/quick-start/
"""


class myspider:
    def __init__(self, seeds):
        self.current_deepth = 1
        self.linkQuence = linkQuence()
        if isinstance(seeds, str):
            self.linkQuence.addUnVisted(seeds)
        if isinstance(seeds, list):
            for i in list:
                self.linkQuence.addUnVisted(i)
        print "Add the seeds url \"%s\" to the unvisited url list" % str(self.linkQuence.unvisted)

    def getHtml(self, url, tries=3):
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        try:
            response = s.get(url, verify=False)
        except requests.exceptions.ConnectionError, e:
            print e
        return (response.status_code, response.text)

    def saveImage(self, imgurl):
        imageName = "".join(imgurl.split('/'))
        imgurl = 'http://kubernetes.io' + imgurl
        response = requests.get(imgurl)
        image = response.content
        Dir = "/home/nuan/Pictures/docker/"
        print "Image save as " + Dir + imageName
        try:
            with open(Dir + imageName, "wb") as jpg:
                jpg.write(image)
        except IOError:
            print "IOError"
        finally:
            jpg.close()

    def getLinks(self, url):
        links = []
        response = self.getHtml(url)
        if response[0] == 200:
            soup = BeautifulSoup(response[1], "lxml")
            alist = soup.findAll("a", {'href': re.compile('/docs/')})
            for a in alist:
                if a['href'].find("/docs/") != -1:
                    # print a['href']
                    link = 'http://kubernetes.io' + a['href']
                    links.append(link)
            imageList = soup.findAll("img")
            for img in imageList:
                if img['src'].find('/images/') != -1:
                    # print img['src']
                    self.saveImage(img['src'])

        return links

    def crawling(self, seeds, crawl_deepth):
        while self.current_deepth <= crawl_deepth:
            linklist = []
            index = 0
            while not self.linkQuence.UnvistedISEmpty():
                index += 1
                url = self.linkQuence.UnVistedDeQue()
                print "Pop out one url \"%s\" from unvisited url list" % url
                links = self.getLinks(url)
                for l in links:
                    linklist.append(l)
                print "Get %d new links" % len(links)
                self.linkQuence.addVisted(url)
                print "Visited url count: " + str(self.linkQuence.getvistedCount())
                print "Visited deepth: " + str(self.current_deepth) + "index:" + str(index)
            for link in linklist:
                self.linkQuence.addUnVisted(link)
            print "%d unvisited links:" % (self.linkQuence.getUnvisteCount())
            self.current_deepth += 1


class linkQuence():
    def __init__(self):
        self.visted = []
        self.unvisted = []

    def getVisted(self):
        return self.visted

    def getUnvisted(self):
        return self.unvisted

    def addVisted(self, url):
        self.visted.append(url)

    def addUnVisted(self, url):
        if url != "" and url not in self.visted and url not in self.unvisted:
            self.unvisted.append(url)

    def UnVistedDeQue(self):
        try:
            return self.unvisted.pop()
        except:
            return None

    def getvistedCount(self):
        return len(self.visted)

    def getUnvisteCount(self):
        return len(self.unvisted)

    def UnvistedISEmpty(self):
        return len(self.unvisted) == 0


def main(seeds, deepth):
    spider = myspider(seeds)
    spider.crawling(seeds, deepth)


if __name__ == '__main__':
    if __name__ == '__main__':
        main("http://kubernetes.io/docs/", 3)
        # main("https://docs.docker.com/", 2)
