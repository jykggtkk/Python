#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
#脚本功能：校验数据文本，检查每行字段个数是否匹配数据库表字段个数,并对存在的非法换行符进行替换
#输入参数：文本名称带绝对路径，正确的字段个数校验值，分隔符字符
#初次编写日期：2017-01-23
#说明：    整合check功能和替换功能，其中特别说明，替换策略默认首字段不会出现换行符，否则逻辑陷阱
           无法解决最后一个字段存在换行符时具体换行后的数据归属上一行最后一个字段还是下一行第一个
           字段
           函数化检查和替换，便于重复调用
#测试：    还有一些情况可能不支持，暂时没办法了： 比如一行多个字段有回车符的情况
'''
import sys
import os
import time
#函数1，判断是否为空文件
def  checkFileNull(fileName):
    checkFile=open(fileName)
    num=len(checkFile.read())
    if num==0:
      noneFlag=1
    else:
      noneFlag=0
    checkFile.close()
    return noneFlag
#函数2，判断首行分隔符个数是否正确
def  checkFirstLine(fileName,checkNum,splitStr):
    checkFile=open(fileName)
    #1.0.5获取首行字段分隔符个数
    realNum=checkFile.readline().count(splitStr)
    return realNum
#函数3，判断每一行分隔符是否正确,只判断不替换
def  checkLines(fileName,checkNum,splitStr):
    checkFile=open(fileName)
    lineNumber=0
    lines=checkFile.readlines()
    for line in lines:
        if not line:
            break
        if line.count(splitStr)!=checkNum:
            lineNumber=lineNumber+1
            splitNumber=line.count(splitStr)
            checkFlag=1
            break
        else:
            lineNumber=lineNumber+1
            splitNumber=checkNum
            checkFlag=0
    resultDict={'lineNumber':lineNumber,'splitNumber':splitNumber,'checkFlag':checkFlag}
    checkFile.close()
    return resultDict
#函数4，替换，替换完毕后继续调用checkLines进行检查新文件
def  replaceLines(fileName,checkNum,splitStr):
    #打开文件和目标文件
    checkFile=open(fileName)
    targetFile=open(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".change",'w')
    lines=checkFile.readlines()
    lineNumber=0
    #一开始写关闭
    writeFlag=0
    #与上一行合并的需要获取上一行数据
    tempLine = ""
    #额外获取一行后还是要 0 不跳
    skipFlag=0
    #中间是否打印标识 0打印
    middleFlag=0
    #中间字段多换行符标识
    downEndFlag=0
    #中间字段出现换行符时第一次不重复写标识
    firstFlag=0

    for line in lines:
        if not line:
            break
        elif line.count(splitStr)==0:
            #分隔符为0，那么前面那行就不能写到目标文本里去
            writeFlag=0
            #将上一行跟本行合并
            #当中间某字段多个换行符时，属于非末尾字段换行情况的，要略过这一步，否则会导致数据重复
            if(firstFlag==0):
                tempLine=tempLine+line.replace("\n","")
            middleFlag=0
            firstFlag=0
        elif line.count(splitStr) < checkNum and line.count(splitStr) > 0:
            #分隔符为大于0时，可以判定前面那行可以写进去（即使不等于checkNum，上一行也已经正确
            writeFlag=1
            newLine=tempLine
            if(skipFlag==0):
                #只出现一个字段多个换行的时候
                #出现多个换行符的时候，下一行
                if(downEndFlag==0):
                    tempLine=line.replace("\n","")+getDownLine(fileName,lineNumber)
                    if(tempLine.count(splitStr)!=checkNum):
                        #第一次合并了下一行后检查还是不够，说明还存在分隔符，需要跟下一行合并
                        '''print "STILL WRONG"'''#调试用代码
                        downEndFlag=1
                        firstFlag=1
                #下一行要跳过
                skipFlag=1
                middleFlag=0    
            else:
                #其实，当该字段出现多个换行符时，最后一个在替换前的skipFlag状态位一定是：1，因为其他换行符的处理都在第一个if流程里走了 未重置skipFlag
                #因此最后一步替换可以放在skipFlag=1的情况下处理，处理完再判断downEndFlag
                #该行跳过打印，但当 if(downEndFlag==1)时，还是要把本行并到tempLine里去的  
                """if(downEndFlag==1):
                    tempLine=tempLine+line.replace("\n","")
                    #如果这次合并之后没问题了  downEndFlag就置0
                    if(tempLine.count(splitStr)==checkNum):
                        print "合并分隔符个数对了"
                        downEndFlag=0"""
                #一个字段多次换行的情况，最后一次就走这里那必然分隔符是对的了
                if(downEndFlag==1 and tempLine.count(splitStr) + line.count(splitStr)==checkNum):
                    tempLine=tempLine+line.replace("\n","")
                    '''print " ONE COLUMN CHANGE RIGHT"'''#调试用代码
                    downEndFlag=0
                #多字段存在分隔符情况,依据是合并后的分隔符还是不能跟检查值匹配，但还是有漏洞
                elif(downEndFlag==1 and tempLine.count(splitStr) + line.count(splitStr)!=checkNum):
                    tempLine=tempLine+getDownLine(fileName,lineNumber)
                    if(tempLine.count(splitStr)==checkNum):
                        '''print " MUTTLE COLUMNS RIGHT"'''#调试用代码
                        downEndFlag=0
                    else:
                        '''print " MUTTLE COLUMNS STILL WRONG"'''#调试用代码
                        downEndFlag=1
                #打印
                skipFlag=0
                middleFlag=1
        elif line.count(splitStr)==checkNum:
            #分隔符为大于0时，可以判定前面那行可以写进去（即使不等于checkNum，上一行也已经正确
            writeFlag=1
            newLine=tempLine
            tempLine=line.replace("\n","")
            middleFlag=0
        else:
            pass
        #满足标识条件才能写 #调试用代码
        '''print "writeFlag:"+str(writeFlag)
        print "lineNumber:"+str(lineNumber)
        print "downEndFlag:"+str(downEndFlag)
        print "skipFlag:"+str(skipFlag)
        print "middleFlag:"+str(middleFlag)
        print "firstFlag:"+str(firstFlag)
        print "newLine:"+newLine
        print "tempLine:"+tempLine
        print "line:" +line'''
        #打印中间结果，第一行因为newline还没有值不打印
        if(writeFlag==1 and lineNumber>0 and middleFlag==0):
            '''print "MIDDLE PUTLINE newLine:"+newLine'''
            targetFile.write(newLine+"\n")
            #再置回默认值
            writeFlag=0
        lineNumber=lineNumber+1
    #最后一行数据额外打印
    '''print "LAST PUTLINE tempLine:"+tempLine''' #调试用代码
    targetFile.write(tempLine+"\n")
    #关闭文件
    checkFile.close()
    targetFile.close()
    #文件替换
    if(os.path.isfile(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".delete")):
        os.remove(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".delete")
    os.rename(fileName, os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".delete")
    os.rename(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".change", fileName)

#函数5，获取对应行数的下一行数据
def getDownLine(fileName,errorLine):
    checkFile=open(fileName)
    line=checkFile.readlines()[errorLine+1]
    line=line.replace("\n", "")
    checkFile.close()
    return line

def main():
    fileName=sys.argv[1]
    checkNum=int(sys.argv[2])
    splitStr=sys.argv[3]

    #checkNum 需要减1
    checkNum=checkNum-1

    #确定输入的是文件名
    if(os.path.isfile(fileName)): 
        #1.0检查文件是否为空文件，空文件无需再检查直接退出
        noneFlag=checkFileNull(fileName)
        if noneFlag==1:
            print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"[INFO]The file is null!"
            sys.exit(0)
        #2.0检查首行字段个数是否正确,首字段个数不对直接退出，可能是文本结构与登记结构不一致
        realNum=checkFirstLine(fileName,checkNum,splitStr)
        if realNum!=checkNum:
            print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+str("[ERROR]The checked result is wrong,correct number should be %d,but the actual number is %d"%(checkNum+1,realNum+1))
            sys.exit(1)
        #3.0检查每行字段个数是否正确
        resultDict=checkLines(fileName,checkNum,splitStr)
        #4.0 返回正确结果
        if resultDict['checkFlag']==0:
            print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+str("[INFO]The checked result is right,actual number is %d"%(int(resultDict['splitNumber'])+1))
            sys.exit(0)
        else:
            #调用替换函数
            replaceLines(fileName,checkNum,splitStr)
            #文件继续检查
            resultDictNew=checkLines(fileName,checkNum,splitStr)
            if resultDictNew['checkFlag']==0:
                print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+str("[INFO]After replace operate,the checked result is right,actual number is %d"%(int(resultDictNew['splitNumber'])+1))
                sys.exit(0)
            else:
                print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"[ERROR]After replace operate,the actual number is still wrong!"
                sys.exit(1)
    else:
        print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"[ERROR]The file not exists!"
        sys.exit(1)

if __name__ == '__main__': 
    #设置环境编码
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()