#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
脚本功能：批量文件转码
脚本说明：依赖python工具：chardet
          实际应用中不建议使用codec读取源文件编码，如能确定最好先指定好源文件编码格式，读取编码格式特别慢
          GB18030能解析GBK GB2312的所有字符；空文件不转码直接转存
输入参数：待转码文本名或路径，文件生成路径
初次编写日期：2016-03-02
编写人：  duwj
更新日期：2016-03-03
更新版本：v1.1
更新内容：
          1.脚本分离，读取文本编码格式功能分出来，实际应用无法接受读取编码的耗时，转码脚本只接受参数
          2.不同编码格式的文本转码操作不一样，像空文本和anscii码的文本都无需转码直接转移
          3.脚本名称已修改
'''
import os
import sys
import chardet
import codecs
import shutil
#修改编码格式
def changeEncoding(path,targetPath,sourceEncoding,backup=False):
    result=True
    try:
        #None  utf-8  anscii文本均无需处理
        if get_size(path)==0:
            shutil.copyfile(path,targetPath+"/"+str(path).split("/")[-1])
        elif get_size(path)!= 0 and cmp(sourceEncoding,"ascii")==0:
            shutil.copyfile(path,targetPath+"/"+str(path).split("/")[-1])
        elif get_size(path)!= 0 and cmp(sourceEncoding,"utf-8")==0:
            shutil.copyfile(path,targetPath+"/"+str(path).split("/")[-1])
        else:
            filename=str(path).split("/")[-1]
            print "file's name =",filename 
            #采用兼容范围更广的编码格式：
            if cmp(sourceEncoding,"GB2312")==0:
                sourceEncoding ="GB18030"
                print "set sourceEncoding =",sourceEncoding
            sourceFile=codecs.open(path,"r",sourceEncoding)
            lines=sourceFile.readlines()
            #写入目标文件
            targetFile=codecs.open(str(targetPath)+"/"+filename,"w")
            #正常情况下解码
            for x in lines: 
                targetFile.write(x.decode('UTF-8','ignore'))
            print("conver file:%s,source encoding:%s,target encoding:%s"%(path,sourceEncoding,"UTF-8"))
    except Exception  as err:
        print(err)
        result=False
        print("convert file encoding failed,file:%s.\ncause:%s"%(path,err))
    finally:  
        if os.path.exists(str(path)) and result:
            sourceFile.close()
            targetFile.close() 
        elif os.path.exists(str(path)) and not result:
            sourceFile.close()
            targetFile.close() 
#获取编码格式
def get_charset(file):
    temp=file.read()
    return chardet.detect(temp)['encoding']

#获取文件大小
def get_size(file):
    return os.path.getsize(file)

#遍历目录下的文件并转码
def explore(dir,targetPath,sourceEncoding):
    for root,dirs,files in os.walk(dir):
        for file in files:
            path=os.path.join(root,file)
            #print path,":" 
            changeEncoding(path,targetPath,sourceEncoding)

#主方法
def main():
    sourcePath=sys.argv[1]
    targetPath=sys.argv[2]
    sourceEncoding=sys.argv[3]

    if   (os.path.isfile(sourcePath)):
            changeEncoding(sourcePath,targetPath,sourceEncoding)
    elif os.path.isdir(sourcePath):
            explore(sourcePath,targetPath,sourceEncoding)

 
if __name__ == '__main__': 
    #设置环境编码
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()
     
  
