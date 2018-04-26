#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
import datetime 
from time import ctime,sleep


acctnoarr=[]
datearr=[]
tranbrarr=['001001','001002','001003','001004','001005']
trantparr=['CS','TR']


#获取账号列表
def getAcctnoArr():
    for i in range(10000):
        acctno= '6213'+str(random.randint(100000000000,99999999999999))
        acctnoarr.append(acctno)

#获取流水号列表
def getTransqArr():
    randomdata = range(10000000,99999999)  
    randomlist  = random.sample(randomdata,100000) #实际每天需要100w
    
    return  randomlist

#获取时间列表
def getDate():
    begin = datetime.date(2017,6,1)  
    end = datetime.date(2017,6,1)
    d = begin
    delta = datetime.timedelta(days=1)  
    while d <= end:  
        d.strftime("%Y%m%d")
        datearr.append(d.strftime("%Y%m%d"))
        d += delta
#主方法
def main():

    #数据文件名称
    resultFile="kn_kns_tran"
    getAcctnoArr()
    getDate()  
    for date in datearr:
        i=1
        #打开一个待写入的文件
        file=open(resultFile+str(date)+".txt",'a+')
        #生成随机流水号
        transqarr=getTransqArr()
        #生成N条数据
        while i<=10000:
            #获取日期
            trandt=date
            #获取流水号
            #print "i"+str(i)
            #print len(transqarr)
            transq=random.choice(transqarr)
            transqarr.remove(transq)
            #获取时间
            tranti=str(random.randint(0,23))+str(random.randint(10,60))+str(random.randint(10,60))
            if len(tranti)<6:
                tranti ='0'+tranti
            else:
                pass

            #获取交易种类
            trantp =random.choice(trantparr)

            #获取交易部门
            tranbr =random.choice(tranbrarr)
            #获取交易币种
            crcycd='01'
            #获取交易金额
            tranam=round(random.uniform(0, 99999),2)
            #获取交易账号
            acctno=random.choice(acctnoarr)
            #获取交易对手方账号
            toacct=random.choice(acctnoarr)
            if toacct==acctno:
                toacct=random.choice(acctnoarr)

            file.write(str(trandt)+"~"+str(transq)+"~"+str(tranti)+"~"+str(trantp)+"~"+str(tranbr)+"~"+str(crcycd)+"~"+str(tranam)+"~"+str(acctno)+"~"+str(toacct)+"\n")
            i=i+1
        #完成后关闭文件
        file.close()

if __name__ == '__main__': 
    #设置环境编码
    reload(sys)
    sys.setdefaultencoding('utf8')
    print "begin: %s" %ctime()
    main()
    print "all over %s" %ctime()