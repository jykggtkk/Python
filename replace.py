#!/usr/bin/python
#coding=utf-8
'''
脚本功能：  主要对源系统导出的数据文件进行校验后，对出现的字段值中的换行符进行处理，
           处理有两种选择 一种是直接删除，另一种是用特殊字符替换掉
关注点：    字符读取替换后的再次判断
编写：      duwj
初次编写日期：2016-03-10
遗留问题：   如果是一个字段里出现多个回车符，而字符串字段又不是像用“”括起来的，数据文件处理后会发生数据错误，
           有双引号应该就没问题，待后续想想
'''
import sys
import os
import shutil

path=sys.argv[1]
cnt=int(sys.argv[2])
splitstr=sys.argv[3]
filename=str(path).split("/")[-1].split(".")[0]
targetfilename=filename+"_rp.txt"
file=open(path)
lines=file.readlines()
#num=len(file.read())
#print num
temp=""
#if num==0:
#    file.close()
#    shutil.copyfile(path,str(filename)+"_rp.txt")
#    print(" file is empty,file:%s"%(str(path)
#检查每行的字段分隔符个数是否正确，如果正确就直接读取写入到另一个文本，否则进行处理
targetFile = open(targetfilename,'w')
for line in lines:
    if not line:
        print "-----------------"
        break
    #与上一行合并
    strl=str(line)
    strl=temp+strl
    #每行字段个数符合表结构，同时双引号成对出现
    #print "strl:",strl
    #print "temp:",temp
    #print strl.count(splitstr), strl.count("\"")%2
    if strl.count(splitstr)==cnt and strl.count("\"")%2==0:
        temp=""
        #正常值写入新文件
        targetFile.write(strl)
    elif strl.count(splitstr)==cnt and strl.count("\"")%2==1:
        temp=strl.replace("\n", "")
        continue
    else:
        #strl.count(splitstr)!=cnt:
        temp=strl.replace("\n", "")
        continue
print "[INFO]文件修改成功，新生成文件：",str(filename)+"_rp.txt"
targetFile.close()
file.close()
