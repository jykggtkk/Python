# -*- coding: utf-8 -*-
'''
爬虫url Html下载器
'''
import urllib2
class HtmlDownloader(object):
    
    def download(self,url):
        if url is None:
            return None 

        response = urllib2.urlopen(url)

        if response.getcode()!=200:
            print  "wrong!"
            return None 

        return response.read()

        

    