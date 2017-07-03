#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Script function: Check the data text,determine the number of fields in every rows 
whether can match the number of database table fields or not.In some scenarios can 
repair the data text by merging rows.finally if it can't be repaired then output 
the error messages.

Instruction：Integrate the functions of check.py and repair.py.specially,the repair
function can work in only this scenario: The first field does not appear to have 
newline characters,otherwise it can't be detemined whether the rows that the number 
of the separators is zero is belong to the previous row or the latter one.That is a 
logical trap.Besides,the replace def can run only once a time,and check def
can run only twice a time.If the file still wrong,then just warn.

Parameters: Text name with absolute path;The correct number of database table fields;
separator character.For example:
python checkReplace.py  /mdp/odm/kn/kn_kna_acct.txt 20 ~@~

Bugs: In Some scenarios there is some problems,when using it please be careful:
      1.when used in linux environment, separator character ~ can't be support by 
      the check function.Maybe some other character too.  


First code date：2017-01-23

Last update : 2017-07-03

Author: duwj@sunline.cn
'''
import sys
import os
import time

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
    checkFile=open(fileName)
    targetFile=open(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".change",'w')
    lines=checkFile.readlines()
    lineNumber=0
    linesNumber=len(lines)
    
    writeFlag=0 #写标识 1为可写
    tempLine = "" #临时组装行，也是上一行
    writeLine = "" #会写入的值
    readLines=[]
    lineNumberInner=0
    for line in lines:
        if not line:
            pass
        elif lineNumber == linesNumber:
            pass
        elif line.count(splitStr)==0:
            if lineNumber < lineNumberInner:
                tempLine="" #清空tempLine
                pass
            else:
                #该行为0，则只要单纯的把该行并入到上一行
                tempLine=tempLine+line.replace("\n","")

                #如果这行满足分隔符条件
                if tempLine.count(splitStr)==checkNum:
                    #只要下一行不是单字符的，可以写入;否则就过，继续合并
                    if getNextLine(fileName,lineNumber).count(splitStr)>0:
                        writeLine=tempLine
                        writeFlag=1
                    else:
                        pass

        elif line.count(splitStr) < checkNum and line.count(splitStr) > 0:
            #这行既不是合法的也不是单字符的，说明有截断
            #截断的数据考虑怎么弄呢，就是将他们恢复后存到一个临时租赁里，不写入，最后再写

            tempLine = line.replace("\n","")
            #如果该行被合并过，最好是跳过它
            if lineNumber < lineNumberInner:
                #print "lineNumberInner:"+str(lineNumberInner)
                tempLine="" #清空tempLine 
                pass
            else:
                lineNumberInner=lineNumber
                while lineNumberInner < linesNumber:
                    if getNextLine(fileName,lineNumberInner).count(splitStr)==checkNum:
                        break
                    else: 
                        #如果连续两行都出现换行的情况需要考虑
                        if tempLine.count(splitStr) == checkNum:
                            if getNextLine(fileName,lineNumberInner).replace("\n","").count(splitStr)==0:
                                tempLine=tempLine+getNextLine(fileName,lineNumberInner).replace("\n","")
                                lineNumberInner=lineNumberInner+1                           
                            else:
                                #加1后再跳出
                                lineNumberInner=lineNumberInner+1
                                break
                        else:
                            tempLine=tempLine+getNextLine(fileName,lineNumberInner).replace("\n","")
                            lineNumberInner=lineNumberInner+1
                      
                if tempLine.count(splitStr) == checkNum:
                    readLine=tempLine
                    readLines.append(readLine)
                else:
                    pass
        elif line.count(splitStr)==checkNum:
            #writeFlag=1  #When the number of separators is greater than 0, the previous line can be printed
            tempLine=line.replace("\n","")
            #如果下一行没有单个字符，也就是下一行至少有一个分隔符，那么这行就可以写入了
            if getNextLine(fileName,lineNumber).count(splitStr)>0 :
                writeLine=tempLine
                writeFlag=1
            #说明下一行是该行的一部分，不能写入
            else:
                writeFlag=0
        else:
            pass
        #Only can be printed when satisfy all condition
        '''
        #debug
        print "writeFlag:"+str(writeFlag) +" = 1"
        print "OUTER-lineNumber:"+str(lineNumber) +" > 0 "
        print "writeLine:"+writeLine
        print "tempLine:"+tempLine
        print "line:" +line
        #'''

        if(writeFlag==1):
            '''print "==================================="
            print "write line:"+writeLine
            print "now lineNumber = " +str(lineNumber)
            print "==================================="'''
            targetFile.write(writeLine+"\n")
            #back to 0 
            writeFlag=0
        lineNumber=lineNumber+1
    #把错误行都写进去
    for line in readLines:
        targetFile.write(line+"\n")

    #Output the last line.
    lastLine=tempLine
    if lastLine == writeLine or lastLine.count(splitStr)<checkNum:
        pass
    else:
        '''print "==================================="
        print "write last line:"+lastLine
        print "now lineNumber = " +str(lineNumber)
        print "==================================="'''
        targetFile.write(lastLine+"\n")


    print "The changed lines:" +str(readLines)
    checkFile.close()
    targetFile.close()
    #replace file
    if(os.path.isfile(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".delete")):
        os.remove(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".delete")
    os.rename(fileName, os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".delete")
    os.rename(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".change", fileName)

#def five:get next line 
def getNextLine(fileName,errorLine):
    checkFile=open(fileName)
    line=""
    try:
        line=checkFile.readlines()[errorLine+1]
        line=line.replace("\n", "")
        checkFile.close()
    except:
        print "It's last line,lineNumber="+str(errorLine+1)
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
            print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"[INFO]The file is null!"
            sys.exit(0)
        #2.0 Determine whether the number of separators is correct in the first row. 
        #if not,Exit and output error messages 
        realNum=checkFirstLine(fileName,checkNum,splitStr)
        if realNum!=checkNum:
            print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+str("[ERROR]The checked result is wrong,correct number should be %d,but the actual number is %d"%(checkNum+1,realNum+1))
            sys.exit(1)
        #3.0 Determine whether the number of separators is correct in every rows
        resultDict=checkLines(fileName,checkNum,splitStr)
        #4.0 return the right result
        if resultDict['checkFlag']==0:
            print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+str("[INFO]The checked result is right,actual number is %d"%(int(resultDict['splitNumber'])+1))
            sys.exit(0)
        else:
            #call the replace function 
            replaceLines(fileName,checkNum,splitStr)
            #countinue to check 
            resultDictNew=checkLines(fileName,checkNum,splitStr)
            if resultDictNew['checkFlag']==0:
                print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+str("[INFO]After replace operate,the checked result is right,actual number is %d"%(int(resultDictNew['splitNumber'])+1))
                sys.exit(0)
            else:
                print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"[ERROR]After replace operate,the actual number is still wrong!"
                print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"[ERROR]The number of the wrong line is " +str(resultDictNew['lineNumber'])
                sys.exit(1)
    else:
        print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"[ERROR]The file not exists!"
        sys.exit(1)

if __name__ == '__main__': 
    #Setting environment character set
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()
