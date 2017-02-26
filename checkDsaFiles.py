#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
#脚本功能：校验供数数据文本，检查每个文件大小及记录数，登记入统一文本
#输入参数：系统英文简称/批次日期
#初次编写日期：2017-02-25
#说明：基于验证平台供数文件每日对比的需求，非文件相同比较
#测试记录：
#修改记录：
'''
import os
import sys
import shutil
import time
import chardet

#检查文件并返回检查结果
def checkFile(path):
    try:
        #获取系统简称
        systemName=str(path).split("/")[-2]
        #print "systemName:",systemName
        dataDate=os.path.dirname(path).split("/")[-1]
        #print "pathName:",pathName
        #获取文件名称  LINUX下要改\\为/
        fileName=str(path).split("/")[-1].split("\\")[-1]
        #print "fileName:",fileName
        #获取文件大小
        fileSize = getSize(path)
        #print "fileSize:",fileSize
        #获取文件源编码格式 --会很慢 考虑去掉
        file=open(path,"rb")
        fileEncod=getCharset(file)
        #fileEncod="utf-8"
        #获取文件总行数
        fileNum = 0
        for i in file:
            fileNum += 1
        file.close()
        #写入resultDict
        resultDict={'systemName':systemName,'dataDate':dataDate,'fileName':fileName,'fileSize':fileSize,'fileNum':fileNum,'fileEncod':fileEncod}
        print resultDict
        #print str(resultDict['systemName'])+"~@~"+str(resultDict['dataDate'])+"~@~"+str(resultDict['fileName'])+"~@~"+str(resultDict['fileSize'])+"~@~"+str(resultDict['fileNum'])+"~@~"+str(resultDict['fileEncod'])+"~@~"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        return  resultDict

    except Exception  as err:
        print(err)
    finally:  
        file.close()
#获取编码格式
def getCharset(file):
    return chardet.detect(file.read())['encoding']
#读取文件大小
def getSize(file):
    return '%d'%(os.path.getsize(file))

#遍历目录下的文件
def explore(dir):
    for root,dirs,files in os.walk(dir):
        for file in files:
            fileName=os.path.join(root,file)

            #检查每个文件
            resultDict=checkFile(fileName)

            #目标文件
            dataDate=os.path.dirname(fileName).split("/")[-1]

            resultFile="E:\\dsa/checkFileResult"+dataDate.replace("-","")+".check"

            #需要避免数据重复--插入前先检索之前是否有记录有则删除
            #或者是增加标记字段，将该行记录失效  
            #以上 待想想

            #追加数据
            file=open(resultFile,'a+')
            file.write(str(resultDict['systemName'])+"~@~"+str(resultDict['dataDate'])+"~@~"+str(resultDict['fileName'])+"~@~"+str(resultDict['fileSize'])+"~@~"+str(resultDict['fileNum'])+"~@~"+str(resultDict['fileEncod'])+"~@~"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"\n" )
            file.close()
'''
            if(os.path.isfile(resultFile)):
                #需要避免数据重复--插入前先检索之前是否有记录有则删除
                #code

                file=open(resultFile,'a')
                file.write(str(resultDict['systemName'])+"~@~"+str(resultDict['dataDate'])+"~@~"+str(resultDict['fileName'])+"~@~"+str(resultDict['fileSize'])+"~@~"+str(resultDict['fileNum'])+"~@~"+str(resultDict['fileEncod'])+"~@~"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"\n" )
            else:
                file=open(resultFile,'w')
                file.write(str(resultDict['systemName'])+"~@~"+str(resultDict['dataDate'])+"~@~"+str(resultDict['fileName'])+"~@~"+str(resultDict['fileSize'])+"~@~"+str(resultDict['fileNum'])+"~@~"+str(resultDict['fileEncod'])+"~@~"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"\n"  )
'''
#主方法
def main():
    sysName=sys.argv[1]
    dataDate=sys.argv[2]

    #拼接目录
    checkPath="E:\\dsa/"+sysName+"/"+dataDate.replace("-","")

    #遍历目录进行读取并写入文本
    if os.path.isdir(checkPath):
        explore(checkPath)
    else:
        print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+str("[ERROR]The directory is not exists:%s"%(checkPath))
        sys.exit(1)


    print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+str("[INFO]Check is over")
    sys.exit(0)

if __name__ == '__main__': 
    #设置环境编码
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()