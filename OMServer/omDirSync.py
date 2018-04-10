#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
脚本名称：omDirSync.py
脚本功能：比较两个目录的内容是否一致，不一致自动更新同步
脚本说明：比较两个目录的内容是否一致，不一致自动更新同步
输入参数：目录
初次编写日期：2016-08-17
编写人：  
更新日期：
更新版本：
更新内容：         
'''

import os
import sys
import filecmp
import re
import shutil

#待更新列表
holderList=[]


#递归获取更新项
def compareMe(orgDir,tarDir):
	dirComp=filecmp.dircmp(orgDir,tarDir)
	#源目录新文件或者目录
	onlyInOne=dirComp.left_only
	#不匹配文件，源目录文件已发生变化
	diffInOne=dirComp.diff_files
	#定义源目录绝对路径
	orgPath=os.path.abspath(orgDir)
	#将更新文件名或目录追加到holderlist
	[holderList.append(os.path.abspath(os.path.join(orgDir,x))) for x in onlyInOne]
	[holderList.append(os.path.abspath(os.path.join(orgDir,x))) for x in diffInOne]
	#判断是否存在相同子目录，以递归
	if len(dirComp.common_dirs) > 0:
		#递归子目录
		for item in dirComp.common_dirs:
			compareMe(os.path.abspath(os.path.join(orgDir,item)),os.path.abspath(os.path.join(tarDir,item)))
	return holderList

#同步路径内容
def dirSync(orgDir,tarDir):
	#对比源目录与备份目录
	sourceFiles=compareMe(orgDir,tarDir)
	orgDir=os.path.abspath(orgDir)

	if not tarDir.endswith('/'): 
		#备份目录路径加'/'
		tarDir=tarDir+'/'
	tarDir=os.path.abspath(tarDir)
	destinationFiles=[]
	createDirBool=False


	#遍历返回的差异文件或目录清单
	for item in sourceFiles:
		#print item
		#将源目录差异路径清单对应替换成备份目录
		destinationDir=re.sub(orgDir,tarDir,item)
		#print destinationDir
		destinationFiles.append(destinationDir)
		#如果差异路径是个目录且不存在，则创建目录
		if os.path.isdir(item):
			if not os.path.exists(destinationDir):
				os.makedirs(destinationDir)
				#再次调用 compareMe 标识
				createDirBool=True

	#重新调用 compareMe函数，重新遍历新创建目录的内容
	if createDirBool:
		destinationFiles=[]
		sourceFiles=[]
		sourceFiles=compareMe(orgDir,tarDir)


		#获取源目录差异路径清单，对应替换成备份目录
		for item in sourceFiles:
			destinationDir=re.sub(orgDir,tarDir,item)
			destinationFiles.append(destinationDir)

	print "Update item:"
	#输出更新列表清单
	print sourceFiles
	#将源目录与备份目录文件清单拆分成元组
	print "target item:"
	print destinationFiles
	copyPair=zip(sourceFiles,destinationFiles)

	for item in copyPair:
		#如果是文件则拷贝文件
		if os.path.isfile(item[0]):
			orgItem=item[0]
			tarPath=item[1]
			shutil.copyfile(item[0],tarPath)


if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf8')
	if len(sys.argv) >2:
		orgDir=sys.argv[1]
		tarDir=sys.argv[2]
	else:
		print "Usage: ",sys.argv[0],"datadir backupdir"
		sys.exit(1)

	#调用同步
	dirSync(orgDir,tarDir)

