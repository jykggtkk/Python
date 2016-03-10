#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
#脚本功能：校验数据文本，检查每行字段个数是否匹配数据库表字段个数
#输入参数：文本名称带绝对路径，正确的字段个数校验值
#初次编写日期：2015-05-15
#更新日期：2016-03-07
#更新版本：v1.2
#更新内容：
#          v1.0
#         1.结构规范化、命名规范化
#         2.支持读取传入变量，使其能够重复利用于不同文本校验
#         3.增加对首行字符个数的判断，如有不匹配提前异常退出
#          v1.1
#         1.增加模块注释
#          v1.2
#         1. 改成根据接收的文本分隔符参数进行校验
'''
#1.0初始化
#1.0.1引入sys模块,支持接入参数并能够传递程序执行状态给shell
import sys
#1.0.2执行结果初始值
flag="ok"
#1.0.3接入变量值，参数0为脚本名称  1 为文件名称  2为字段校验值
scriptname=sys.argv[0]
filename=sys.argv[1]
columnnum=sys.argv[2]
splitstr=sys.argv[3]

#检查是否为空文本
testfile =open(filename)
num=len(testfile.read())
if num==0:
      print(''.join(["                [INFO]file is null,",flag]))
      testfile.close()
      sys.exit(0)
else:
      testfile.close()

#1.0.4打开需校验文本
file = open(filename)
#1.0.5获取首行字段分隔符个数
cnt=file.readlines()[0].count(splitstr)
#1.0.6参数值类型修改
d=int(columnnum)
#1.0.7分隔符个数=字段个数-1
d=d-1
#2.0检查模块
#2.0.1 检查首行字段分隔符个数是否正确，如不匹配，脚本退出返回码为1
if cnt!=d:
        flag="wrong"
        print(''.join(["                [ERROR]check is ",flag]))
        print(''.join(["                [ERROR]the correct value is ",columnnum]))
        print(''.join(["                [ERROR]but the actual value is ",str(cnt+1)]))
        sys.exit(1)
else:
        e="                [INFO]the correct column num is "
        f=''.join([e,str(cnt+1)])
        print(f)
#2.0.2 检查每行的字段分隔符个数是否正确，如不匹配，脚本退出返回码为1
for line in file: 
    if not line:
        break
    if line.count(splitstr)!=cnt:
        flag="wrong"
        print(flag) 
        print("                [ERROR]but some lines'num is ")
        print(line.count(splitstr))
        sys.exit(1)
    else:
        pass
#2.0.3 校验结束，文本关闭
file.close()
print(''.join(["               [INFO]check is ",flag]))
sys.exit(0)
