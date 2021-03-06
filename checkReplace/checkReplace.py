#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Script function: 检查文本确保其每行（每条记录）的字段个数跟实际数据库表的字段个数是一致的，
如不一致可以做一定处理消除多余的换行符,使文本每行字段个数与数据库表变为一致。

Instruction：整合检查和替换两块的功能.替换功能只能在一定前提下工作：
    1.换行符作为记录的分隔符
    2.默认第一个字段不会出现换行,否则无法判断多出来的数据是归属上一行还是下一行的
    3.替换操作只能做一次，一遍替换后仍检查出错必须抛异常去人工反馈错误

    注意：提交生产时，将日志等级改为INFO级别：
    logging.basicConfig(filename='test.log',level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

Parameters: 全路径文本名称；校验的字段个数；分隔符；
For example:
python checkReplace.py  /mdp/odm/kn/kn_kna_acct.txt 20 ~@~

Requirement: logging模块   pip install logging
Bugs: 在某些场景下使用需要注意:
      1.在Linux环境下，分隔符'~'不被支持，无法检查出错误，也许某些其他分隔符也不行。
      2.目前如果文本本身某些行确实缺字段，在替换时会删掉这些缺字段的行导致它校验通过，正在解决
      3.如果连续的两行，第一行少了前几个字段，第二行少了后几个字段或者中间几个字段，两行合起来的字段
      个数正好又符合校验值，那也无法检查出来
      4.最后一行

First code date：2017-01-23

Last update : 2018-04-10

Author: duwj@sunline.cn
'''
import sys
import os
import time
import logging

def  checkFileNull(fileName):
#def one:Determines whether the text is empty
    checkFile=open(fileName)
    num=len(checkFile.read())
    if num==0:
      noneFlag=1
    else:
      noneFlag=0
    checkFile.close()
    return noneFlag

def  checkFirstLine(fileName,checkNum,splitStr):
#def two:Get the number of separators in the first row
    checkFile=open(fileName)
    realNum=checkFile.readline().count(splitStr)
    return realNum

def  checkLines(fileName,checkNum,splitStr):
#def three:Determine whether the number of separators is correct in every rows
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

def  replaceLines(fileName,checkNum,splitStr):
#def four:Merge the wront rows, then call def checkLines to check the new file
    #读取文件内容
    checkFile=open(fileName)
    lines=checkFile.readlines()
    #初始化新的文本
    targetFile=open(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".change",'w')

    #初始参数
    lineNumber=0#初始行数
    linesNumber=len(lines)#总行数
    tempLine = "" #临时组装行，也是上一行
    writeLine = "" #要写入的行
    changeLines=[]  #所有合并修改后的文本行
    wrongLines=[]#错误的文本行
    lineNumberInner=0 #同一行被隔断成多个行时，使用该参数标记内部行数

    #判断位
    writeFlag=0 #写标识 1为可写

    for line in lines:
        nextLine="" #提升性能后这个要改
        if not line:
            pass
        elif lineNumber == linesNumber:
            pass
        elif line.count(splitStr)==0:
            if lineNumber < lineNumberInner:
                tempLine="" #清空tempLine
            else:
                #该行为0，则只要单纯的把该行并入到上一行
                tempLine=tempLine+line.replace("\n","")

                #如果这行满足分隔符条件
                if tempLine.count(splitStr)==checkNum:
                    #只要下一行不是单字符的，可以写入;否则就过，继续合并
                    nextLine=getNextLine(fileName,lineNumber)
                    if nextLine.count(splitStr)>0:
                        #writeLine=tempLine
                        #writeFlag=1
                        readLine=tempLine
                        changeLines.append(readLine)
                    else:
                        pass

        elif line.count(splitStr) < checkNum and line.count(splitStr) > 0:
            #这行既不是合法的也不是单字符的，说明有截断
            #截断的数据考虑怎么弄呢，就是将他们恢复后存到一个临时租赁里，不写入，最后再写

            tempLine = line.replace("\n","")
            #如果该行被合并过，要跳过它
            if lineNumber < lineNumberInner:
                #print "lineNumberInner:"+str(lineNumberInner)
                tempLine="" #清空tempLine
            else:
                lineNumberInner=lineNumber
                while lineNumberInner < linesNumber:
                    InnerNextLine=getNextLine(fileName,lineNumberInner)
                    #如果下一行大于等于检查数值，直接跳出循环，将templine写入changelines
                    if InnerNextLine.count(splitStr)>=checkNum:
                        #readLine=tempLine
                        #changeLines.append(readLine)
                        break
                    #否则，说明下一行应该合并到本行
                    else: 
                        #如果连续两行都出现换行的情况，所以要判断templine是否已经满足要求
                        if tempLine.count(splitStr) >= checkNum:
                            if InnerNextLine.count(splitStr)==0:
                                tempLine=tempLine+InnerNextLine
                                lineNumberInner=lineNumberInner+1
                            else:
                                #加1后再跳出
                                lineNumberInner=lineNumberInner+1
                                break
                        else:
                            tempLine=tempLine+InnerNextLine
                            lineNumberInner=lineNumberInner+1
                      
                if tempLine.count(splitStr) == checkNum:
                    readLine=tempLine
                    changeLines.append(readLine)
                else:
                    #中间的合并结果不会出现在这里
                    #if lineNumberInner
                    wrongLines.append(tempLine)
        elif line.count(splitStr)==checkNum:
            tempLine=line.replace("\n","")
            #如果下一行没有单个字符，也就是下一行至少有一个分隔符，那么这行就可以写入了
            nextLine=getNextLine(fileName,lineNumber)
            if nextLine.count(splitStr)>0 :
                writeLine=tempLine
                writeFlag=1
            #说明下一行是该行的一部分，不能写入
            else:
                writeFlag=0
        else:
            #分隔符大于校验数值i，直接写入
            tempLine=line.replace("\n","")
            readLine=tempLine
            changeLines.append(readLine)
        #只有以下等式都成立才能写
        logging.debug("=logging begin==================================")
        logging.debug("writeFlag:"+str(writeFlag) +" = 1")
        logging.debug("lineNumber:"+str(lineNumber) +" >= 0 ")
        logging.debug("lineNumberInner:"+str(lineNumberInner) +" >= 0 ")
        logging.debug("changeLines:"+str(changeLines))        
        logging.debug("wrongLines:"+str(wrongLines))  
        logging.debug("writeLine:"+writeLine)
        logging.debug("now line:" +line)
        logging.debug("next line:" +nextLine)
        logging.debug("tempLine:"+tempLine)
        logging.debug("=logging end==================================")
        if(writeFlag==1):
            logging.debug("=write==================================")
            logging.debug("write line:"+writeLine)
            logging.debug("now lineNumber = " +str(lineNumber))
            logging.debug("===================================")                
            targetFile.write(writeLine+"\n")
            #back to 0 
            writeFlag=0
            writeLine=""
        lineNumber=lineNumber+1
    #把错误行都写进去
    for line in changeLines:
        targetFile.write(line+"\n")

    #Output the last line.
    lastLine=tempLine
    if lastLine == writeLine or lastLine.count(splitStr)<checkNum:
        pass
    else:
        logging.debug("=write==================================")
        logging.debug("write last line:"+lastLine)
        logging.debug("now lineNumber = " +str(lineNumber))
        logging.debug("===================================")        
        targetFile.write(lastLine+"\n")

    #print "The changed lines:" +str(changeLines)
    logging.debug("The changed lines:" +str(changeLines))
    checkFile.close()
    targetFile.close()
    #replace file
    if len(wrongLines)==0:
        if(os.path.isfile(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".delete")):
            os.remove(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".delete")
        os.rename(fileName, os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".delete")
        os.rename(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".change", fileName)

    return wrongLines

#def five:get next line 
def getNextLine(fileName,errorLine):
    checkFile=open(fileName)
    line=""
    try:
        line=checkFile.readlines()[errorLine+1]
        line=line.replace("\n", "")
        checkFile.close()
    except:
        logging.debug("Next line:It's last line,lineNumber="+str(errorLine+1))
    return line


def main():
    fileName=sys.argv[1]
    checkNum=int(sys.argv[2])
    splitStr=sys.argv[3]

    #the number of separators is equal to the number of fields minus 1
    checkNum=checkNum-1

    #make sure file name 
    if(os.path.isfile(fileName)): 
        #1.0 if the file is empty,exit  
        noneFlag=checkFileNull(fileName)
        if noneFlag==1:
            logging.warning("The "+str(fileName)+" file is null!")
            sys.exit(0)
        #2.0 Determine whether the number of separators is correct in the first row. 
        #if not,Exit and output error messages 
        realNum=checkFirstLine(fileName,checkNum,splitStr)
        if realNum!=checkNum:
            logging.error(str("The "+str(fileName)+" file checked result is wrong,correct number should be %d,but the actual number is %d"%(checkNum+1,realNum+1)))
            sys.exit(1)
        #3.0 Determine whether the number of separators is correct in every rows
        resultDict=checkLines(fileName,checkNum,splitStr)
        #4.0 return the right result
        if resultDict['checkFlag']==0:
            logging.info(str("The "+str(fileName)+" file checked result is right,actual number is %d"%(int(resultDict['splitNumber'])+1)))
            sys.exit(0)
        else:
            #call the replace function 
            wrongMessage=replaceLines(fileName,checkNum,splitStr)
            if len(wrongMessage)>0:
                logging.error("After replace operate,the "+str(fileName)+" file actual number is still wrong! The wrong line is"+str(wrongMessage))
                sys.exit(1)
            #countinue to check 
            resultDictNew=checkLines(fileName,checkNum,splitStr)
            if resultDictNew['checkFlag']==0:
                logging.info(str("After replace operate,the "+str(fileName)+" file checked result is right,actual number is %d"%(int(resultDictNew['splitNumber'])+1)))
                sys.exit(0)
            else:
                logging.error("After replace operate,the "+str(fileName)+" file actual number is still wrong! The number of the wrong line is"+str(resultDictNew['lineNumber']))
                sys.exit(1)
    else:
        logging.error("The "+str(fileName)+" file not exists!")
        sys.exit(1)

if __name__ == '__main__': 
    #初始化环境字符集
    reload(sys)
    sys.setdefaultencoding('utf8')

    #初始化日志配置
    LOG_FORMAT = "%(asctime)s[%(levelname)s]%(message)s"
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S' 
    logging.basicConfig(filename='test.log',level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    #主进程
    main()
