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


#��ȡ�˺��б�
def getAcctnoArr():
    for i in range(10000):
        acctno= '6213'+str(random.randint(100000000000,99999999999999))
        acctnoarr.append(acctno)

#��ȡ��ˮ���б�
def getTransqArr():
    randomdata = range(10000000,99999999)  
    randomlist  = random.sample(randomdata,100000) #ʵ��ÿ����Ҫ100w
    
    return  randomlist

#��ȡʱ���б�
def getDate():
    begin = datetime.date(2017,6,1)  
    end = datetime.date(2017,6,1)
    d = begin
    delta = datetime.timedelta(days=1)  
    while d <= end:  
        d.strftime("%Y%m%d")
        datearr.append(d.strftime("%Y%m%d"))
        d += delta
#������
def main():

    #�����ļ�����
    resultFile="kn_kns_tran"
    getAcctnoArr()
    getDate()  
    for date in datearr:
        i=1
        #��һ����д����ļ�
        file=open(resultFile+str(date)+".txt",'a+')
        #���������ˮ��
        transqarr=getTransqArr()
        #����N������
        while i<=10000:
            #��ȡ����
            trandt=date
            #��ȡ��ˮ��
            #print "i"+str(i)
            #print len(transqarr)
            transq=random.choice(transqarr)
            transqarr.remove(transq)
            #��ȡʱ��
            tranti=str(random.randint(0,23))+str(random.randint(10,60))+str(random.randint(10,60))
            if len(tranti)<6:
                tranti ='0'+tranti
            else:
                pass

            #��ȡ��������
            trantp =random.choice(trantparr)

            #��ȡ���ײ���
            tranbr =random.choice(tranbrarr)
            #��ȡ���ױ���
            crcycd='01'
            #��ȡ���׽��
            tranam=round(random.uniform(0, 99999),2)
            #��ȡ�����˺�
            acctno=random.choice(acctnoarr)
            #��ȡ���׶��ַ��˺�
            toacct=random.choice(acctnoarr)
            if toacct==acctno:
                toacct=random.choice(acctnoarr)

            file.write(str(trandt)+"~"+str(transq)+"~"+str(tranti)+"~"+str(trantp)+"~"+str(tranbr)+"~"+str(crcycd)+"~"+str(tranam)+"~"+str(acctno)+"~"+str(toacct)+"\n")
            i=i+1
        #��ɺ�ر��ļ�
        file.close()

if __name__ == '__main__': 
    #���û�������
    reload(sys)
    sys.setdefaultencoding('utf8')
    print "begin: %s" %ctime()
    main()
    print "all over %s" %ctime()