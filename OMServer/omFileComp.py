#!/usr/lib/python
# -*- coding: utf-8 -*-
'''
脚本名称：omFileComp.py
脚本功能：比较配置文本内容
脚本说明：比较两个文件并输出差异，输出到html文件
输入参数：待比较文件名
初次编写日期：2016-08-17
编写人：  duwj
'''

import difflib
import sys
import os

#读取文件分隔函数
def readFile(filename):
	try:
		fileHandle = open(filename,'rb')
		text=fileHandle.read().splitlines()
		fileHandle.close()
		return text
	except IOError as error:
		print('Read file Error:'+str(error))
		sys.exit(1)
#比较文件
def compareFile(filename1,filename2):
	if filename1=="" or filename2=="":
		print "Usage:om_file_comp.py comfile1 comfile2"
		sys.exit(1)

	lines1=readFile(filename1)
	lines2=readFile(filename2)
	d=difflib.HtmlDiff()
	try:
		htmlFile=str(filename1).split("/")[-1]+'temp.html'
		fileHandle = open(htmlFile,'w')
		t=d.make_file(lines1,lines2)
		fileHandle.write(t)
		fileHandle.close()
	except IOError as error:
		print('Read file Error:'+str(error))
		sys.exit(1)

	#调用修改
	changeCode(filename1+'temp.html')


#修改导出的文件编码格式
def changeCode(filename):
	try:
		tarHtmlFile=str(str(filename).split("/")[-1]).split(".")[0]+'.html'
		orgFileHandle = open(filename,'rb')
		lines=orgFileHandle.readlines()
		tarFileHandle = open(tarHtmlFile,'w')
		for x in lines: 
			tarFileHandle.write(x.replace('charset=ISO-8859-1','charset=UTF8'))
		tarFileHandle.close()
		orgFileHandle.close()
		os.remove(filename)
	except IOError as error:
		print('Read file Error:'+str(error))
		sys.exit(1)
if __name__ == '__main__': 
    #设置环境编码
    reload(sys)
    sys.setdefaultencoding('utf8')

    try:
    	filename1=sys.argv[1]
    	filename2=sys.argv[2]
    except Exception,e:
    	print "Error:" + str(e)
    	print "Usage:omFileComp.py filename1 filename2"
        sys.exit(1) 
    #调用方法
    compareFile(filename1,filename2)
    sys.exit(0)

