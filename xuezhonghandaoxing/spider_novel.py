# coding=utf-8
import requests
import re
import urllib2


# 处理页面标签类
class tool:
    def __init__(self):
        pass

    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>|BiQuKu')
    # 将空格换成空格
    removeSpace = re.compile('&nbsp;&nbsp;&nbsp;&nbsp;')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        x = re.sub(self.removeSpace, "\n\n", x)
        x = re.sub(self.removeSpace, "", x)
        # strip()将前后多余内容删除
        return x


class novel:
    def __init__(self):
        self.base_url = 'http://www.biquku.com/0/761/'
        self.tool = tool()
        self.file = None

    def get_base_page(self):
        request = urllib2.Request(self.base_url)
        page = urllib2.urlopen(request).read().decode('gbk')
        return page

    def get_certain_page(self):
        title = self.get_novel_title()
        cer_url = self.base_url + title[1]
        request = urllib2.Request(cer_url)
        page = urllib2.urlopen(request).read().decode('gbk')
        return page

    def get_content(self):
        page = self.get_certain_page()
        pattern = re.compile('<div id="content">(.*?)</div>', re.S)
        content = re.search(pattern, page)
        contents = self.tool.replace(content.group(1).strip()).encode('utf-8')
        return contents

    def get_character_title(self):
        page = self.get_page()
        pattern = re.compile('<div class="bookname".*?<h1>(.*?)</h1>', re.S)
        content = re.search(pattern, page)
        title = self.tool.replace(content.group(1).strip())
        return title

    def write_file(self):
        title = self.get_novel_title()
        contents = self.get_content()
        self.file = open(title[2] + '.txt', 'w')
        self.file.write(contents)

    def get_novel_title(self):
        page = self.get_base_page()
        pattern = re.compile('<div id="info">.*?<h1>(.*?)</h1>.*?2016.*?<a href=(.*?) target.*?>(.*?)</a>.*?</div>',
                             re.S)
        content = re.findall(pattern, page)
        contents = []
        for item in content:
            # 将小说名存入列表
            contents.append(item[0])
            # 将章节地址存入列表
            contents.append(self.tool.replace(item[1]).replace("\"", ""))
            # 将最新章节名存入列表
            contents.append(item[2])
        return contents


spider_novel = novel()
spider_novel.write_file()
