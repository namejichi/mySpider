__author__ = 'ZY'
# coding:utf-8
import urllib
import urllib2
import re
import os

class duitangSpider:
        def __init__(self):
                self.siteURL = 'http://www.duitang.com/search/?kw=%E5%A4%A9%E6%B6%AF%E6%98%8E%E6%9C%88ol&type=feed&include_fields=top_comments,is_root,source_link,item,buyable,root_id,status,like_count,sender,album&_type=&start='
        def getPage(self,pageIndex,i):
                start = (pageIndex - 1) * 120 + i * 24
                url = self.siteURL + str(start) + "&_=1459911830001"
                request = urllib2.Request(url)
                response = urllib2.urlopen(request)
                return response.read().decode('utf-8')
        def getContents(self,pageIndex):
                contents = []
                #count = 0
                for i in range(0,5,1):
                        page = self.getPage(pageIndex,i)
                        pattern = re.compile(r'<div class="mbpho".*?<a target="_blank" class="a" href=".*?".*?<img data-rootid="(.*?)".*?src="(.*?)".*?<a class="p" target="_blank" href=".*?".*?>(.*?)<.*?<span>.*?<a target="_blank" href=".*?".*?>(.*?)</a>',re.S)
                        items = re.findall(pattern,page)
                        for item in items:
                                contents.append([item[0],item[1],item[2],item[3]])
                                #count = count + 1
                                #print count,item[0],item[1],item[2],item[3]
                return contents
        def mkdir(self,ownerName,albumName):
                ownerName = ownerName.strip()
                albumName = albumName.strip()
                path = 'D:/course/resume/MySpider/' + ownerName + '/' + albumName
                isExists=os.path.exists(path)
                if not isExists:
                        os.makedirs(path)
                        return True
                else:
                        return False
        def saveImg(self,url,ownerName,albumName,imgId,imgType):
                fileName = 'D:/course/resume/MySpider/' + ownerName + '/' + albumName + '/' + str(imgId) + '.' + imgType
                u = urllib.urlopen(url)
                data = u.read()
                f = open(fileName,'wb')
                f.write(data)
                f.close()
        def deleteThumb(self,thumbUrl,imgType):
                s = thumbUrl
                pos1 = s.find('thumb')
                pos2 = s.find(imgType)
                s = s[0:pos1] + s[pos2:]
                return s
        def savePageImg(self,pageIndex):
                contents = self.getContents(pageIndex)
                for item in contents:
                        imgId = item[0]
                        thumbUrl = item[1]
                        sList = thumbUrl.split('.')
                        imgType = sList[-1]
                        url = self.deleteThumb(thumbUrl,imgType)
                        ownerName = item[2]
                        albumName = item[3]
                        self.mkdir(ownerName,albumName)
                        self.saveImg(url,ownerName,albumName,imgId,imgType)
        def savePagesImg(self,start,end):
                for i in range(start,end+1):
                        print 'Downloading the',i,'th page'
                        self.savePageImg(i)
spider = duitangSpider()
spider.savePagesImg(1,8)
