# -*- coding: utf-8 -*-
'''
爬虫url Html输出
'''
import sys

class HTMLOutputer(object):
    def __init__(self):
        self.datas=[]

    

    def collect_data(self,data):
        if data is None:
            return 
        self.datas.append(data)


    def output_html(self):

        fout = open('output.html','w')
        
        fout.write("<html>")
        fout.write("<body>")

        fout.write("<table>")

        #默认 ascii
        for data in self.datas:
            print data['url']
            print data['title'].encode('utf-8')
            print data['summary'].encode('utf-8')
            
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
            fout.write("<td>%s</td>" % data['summary'].encode('utf-8'))
            fout.write("</tr>")


        fout.write("</table>")


        fout.write("</body>")
        fout.write("</html>")
        fout.close()
