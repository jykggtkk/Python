#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
import datetime 

acctnoarr=[]
datearr=[]
tranbrarr=['001001','001002','001003','001004','001005']
trantparr=['CS','TR']


#获取账号列表
def getAcctnoArr():
    for i in range(1000):
        acctno= '6213'+str(random.randint(100000000000,99999999999999))
        acctnoarr.append(acctno)

#获取流水号列表
def getTransqArr():
    randomdata = range(10000000,99999999)  
    randomlist  = random.sample(randomdata,100) #实际每天需要100w
    
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
    getAcctnoArr()
    getDate()
 
    #print acctnoarr
    #print datearr
    #print  len(transqarr)

    for date in datearr:
        i=1
        #生成随机流水号
        transqarr=getTransqArr()
        #生成100条数据
        while i<=10:
            #获取日期
            trandt=date
            #获取流水号
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

            print str(trandt)+"~@~"+str(transq)+"~@~"+str(tranti)+"~@~"+str(trantp)+"~@~"+str(tranbr)+"~@~"+str(crcycd)+"~@~"+str(tranam)+"~@~"+str(acctno)+"~@~"+str(toacct)+"\n" 


if __name__ == '__main__': 
    #设置环境编码
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()