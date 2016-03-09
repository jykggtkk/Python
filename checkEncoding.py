#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
获取各个源系统文件的字符集
脚本功能：获取各个源系统文件的字符集
脚本说明：依赖python工具：chardet
          能够遍历子目录
输入参数：待转码文本名或路径 
初次编写日期：2016-03-02
编写人：  duwj
更新日期：
更新版本：v1.0
更新内容：
'''

import os
import sys
import chardet
import codecs
import shutil  
#修改编码格式
def check_Encoding(path,targetFile):
    result=True
    try:
        #获取系统简称
        systemName=str(path).split("/")[-2]
        #print "systemName:",systemName
        pathName=os.path.dirname(path)
        #print "pathName:",pathName
        #获取文件名称
        fileName=str(path).split("/")[-1]
        #print "fileName:",fileName
        #获取文件大小
        fileSize = get_size(path)
        #print "fileSize:",fileSize
         #获取文件源编码格式
        file=open(path,"rb")
        sourceEncoding=get_charset(file)
        file.close()  
        #print "sourceEncoding:",sourceEncoding
        #写入info 
        info="system's name:"+systemName+";pathName:"+pathName+";file's name:"+fileName+";file's size:"+str(fileSize)+";file's Encoding:"+str(sourceEncoding)+"\n"
        #targetFile.writelines(info.decode('UTF-8','ignore'))
        return  info
      
    except Exception  as err:
        print(err)
        result=False
        print("check file encoding failed,file:%s.\ncause:%s"%(path,err))
    finally:  
        file.close() 
#获取编码格式
def get_charset(file):
    temp=file.read() 
    return chardet.detect(temp)['encoding']

def get_size(file):
    return os.path.getsize(file)

def explore(dir): 
    targetFile=open("/mdp/shell/odm/config/codecs.info","w+")
    for root,dirs,files in os.walk(dir):
        for file in files:
            path=os.path.join(root,file)  
            info=check_Encoding(path,targetFile)
            print info 
            targetFile.writelines(info.decode('UTF-8','ignore'))
    targetFile.close()

def main():
    sourcePath=sys.argv[1] 

    if   (os.path.isfile(sourcePath)):
            change_Encoding(sourcePath)
    elif os.path.isdir(sourcePath):
            explore(sourcePath)
 
 
 
if __name__ == '__main__': 
    #设置环境编码
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()
      
