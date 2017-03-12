# -*- coding: utf-8 -*-
'''
爬虫调度程序
'''
import url_manager,html_downloader,html_parser,html_outputer
class SpiderMain(object):

    #初始化
    def __init__(self):
        self.urls=url_manager.UrlManager()
        self.downloader =html_downloader.HtmlDownloader()
        self.parser=html_parser.HtmlParser()
        self.outputer=html_outputer.HTMLOutputer()

    def craw(self,root_url):
        #辅助信息：当前爬取的序号
        count = 1  
        #将入口url放入待爬取url集合
        self.urls.add_new_url(root_url)
        #当待爬取url集合里有新的url
        while self.urls.has_new_url():
            #存在网页不存在的情况  需要进行异常处理
            try:
                #获取一个新的url
                new_url=self.urls.get_new_url()
                print 'craw %d:%s'%(count,new_url)
                #下载url的内容
                html_cont=self.downloader.download(new_url)
                #分别获取url里的新url和目标数据内容
                new_urls,new_data=self.parser.parse(new_url,html_cont)
                #print new_urls
                #print new_data
                #将新的url加入到待爬取url集合 注意是多个url
                try:
                    self.urls.add_new_urls(new_urls)
                except:
                    print "add_urls wrong"
                #将新的数据输出到内容集合html
                try: 
                    self.outputer.collect_data(new_data)
                except:
                    print "output wrong"

                #满1000推出
                if count == 100:
                    break
                count=count+1

            except:
                print 'craw failed! '

        #输出筛选好的数据
        self.outputer.output_html()



if __name__ == '__main__': 
    #入口URL
    root_url="http://baike.baidu.com/item/Python"

    obj_spider =SpiderMain()
    obj_spider.craw(root_url)

 