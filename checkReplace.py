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
      2.when more than one fields exist newline characters in one row,the repair 
      function can't support it.

First code date：2017-01-23

Last update : 2017-06-17

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
     
    writeFlag=0 #First write off  
    tempLine = "" #template line to merge the previous row and the wrong row
    skipFlag=0 #whether skip the next line or not,first not 
    middleFlag=0 #whether output the templine or not, first not 
    downEndFlag=0 #whether multple newLine characters exist in one of the centre fields or not, first not
    firstFlag=0 #whether need to output in first time when multple newLine characters exist in the centre fields

    for line in lines:
        if not line:
            break
        elif line.count(splitStr)==0:
            writeFlag=0 #the number of separator is 0,that means the previous row is not right,can't be output

            #merge the previous row and this row
            #when it is multple newLine characters in the centre fields maked it's  number of separator
            #is zero.It still can't be output now.Otherwise it cause data duplication.
            if(firstFlag==0):
                tempLine=tempLine+line.replace("\n","")
            middleFlag=0
            firstFlag=0

        elif line.count(splitStr) < checkNum and line.count(splitStr) > 0:
            writeFlag=1#When the number of separators is greater than 0, the previous line can be printed
            newLine=tempLine
            if(skipFlag==0):
                #when  more than one newLine characters exists in one field
                if(downEndFlag==0):
                    tempLine=line.replace("\n","")+getDownLine(fileName,lineNumber)
                    if(tempLine.count(splitStr)!=checkNum):
                        #after once merge,the number is still wrong,that means it nead to merge next line
                        #print "STILL WRONG" #debug
                        downEndFlag=1
                        firstFlag=1
                #skip next line 
                skipFlag=1
                middleFlag=0    
            else:
                if(downEndFlag==1 and tempLine.count(splitStr) + line.count(splitStr)==checkNum):
                    tempLine=tempLine+line.replace("\n","")
                    #print " ONE COLUMN CHANGE RIGHT" #debug
                    downEndFlag=0
                elif(downEndFlag==1 and tempLine.count(splitStr) + line.count(splitStr)!=checkNum):
                    tempLine=tempLine+getDownLine(fileName,lineNumber)
                    if(tempLine.count(splitStr)==checkNum):
                        #print " MUTTLE COLUMNS RIGHT"  #debug
                        downEndFlag=0
                    else:
                        #print " MUTTLE COLUMNS STILL WRONG" #debug
                        downEndFlag=1
                #output open 
                skipFlag=0
                middleFlag=1
        elif line.count(splitStr)==checkNum:
            writeFlag=1  #When the number of separators is greater than 0, the previous line can be printed
            newLine=tempLine
            tempLine=line.replace("\n","")
            middleFlag=0
        else:
            pass
        #Only can be printed when satisfy all condition
        '''
        #debug
        print "writeFlag:"+str(writeFlag)
        print "lineNumber:"+str(lineNumber)
        print "downEndFlag:"+str(downEndFlag)
        print "skipFlag:"+str(skipFlag)
        print "middleFlag:"+str(middleFlag)
        print "firstFlag:"+str(firstFlag)
        print "newLine:"+newLine
        print "tempLine:"+tempLine
        print "line:" +line'''
        #print middle result, skip the first line
        if(writeFlag==1 and lineNumber>0 and middleFlag==0):
            '''print "MIDDLE PUTLINE newLine:"+newLine'''
            targetFile.write(newLine+"\n")
            #back to 0 
            writeFlag=0
        lineNumber=lineNumber+1
    #Output the last line.
    '''print "LAST PUTLINE tempLine:"+tempLine''' #debug
    targetFile.write(tempLine+"\n")

    checkFile.close()
    targetFile.close()
    #replace file
    if(os.path.isfile(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".delete")):
        os.remove(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".delete")
    os.rename(fileName, os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".delete")
    os.rename(os.path.dirname(fileName)+os.path.basename(fileName).split(".")[0]+".change", fileName)

#def five:get next line 
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
                sys.exit(1)
    else:
        print str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"[ERROR]The file not exists!"
        sys.exit(1)

if __name__ == '__main__': 
    #Setting environment character set
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()