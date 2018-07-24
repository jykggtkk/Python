#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
脚本功能：阿拉伯数字与中文数字转换
输入参数：阿拉伯数字,不带符号
初次编写日期：2018-07-24
说明：根据《算法的乐趣提供的算法》
中文数字的权位和小节 
中文数字的特点之一就是每个计数数字都跟着一个权位，这个权位就是数字的量值，相当于阿拉伯数字中的数位。最低位（个位）没有权位，也可以理解为权位为空 
中文数字的另一个特点是以“万”为小节（欧美习惯以“千”为小节），每一个小节都有一个节权位，万以下的没有节权位（或节权位为空），万以上的就是万，再大的就是“亿”，每个小节内部都以“十百千”为权位的独立计数。“十百千”这几个权位是不能连续出现的，如二十百，一千千，但万和亿作为节权位却可以和其他权位一起使用，如二十亿等

中文数字的零 
中文对零的使用总结有以下三条： 
规则1：以10000为小节，小节的结尾即使是0，也不使用“零”。 
规则2：小节内两个非0数字之间要使用“零”。 
规则3：当小节的“千”为是0是，若本小节的前一小节无其他数字，则不用“零”，否则用“零”。

这里蕴含的算法设计模式 我觉得有 分治法 动态规划（状态位）
'''
import os
import sys
import logging

#首先定义对照关系元组

#CHN_NUM_CHAR_COUNT = 10

#单个数字对应的中文汉字
chnNumChar = ("零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖")
#小节位，对32位正数表达的最大整数来说，最大节权万亿就够了
chnUnitSetion = ("", "万", "亿", "万亿")
#每个小节里面的独立计数
chnUnitChar = ("", "拾", "佰", "仟")

def NumberToChinese(num):
    #取每个小节内数据然后节内处理
    #先定义小节的位置，从最低一级的小节开始转换
    unitPos=0
    #定义规则3需不需要补零的状态位，初始默认是不需要补零
    needZero=False
    #初始字符串
    chnStr=""

    while num > 0 :
        strIns=""
        section=num % 10000
        logging.debug( "Now:num: "+str(num) +"section:"+str(section))

        if needZero:
            #满足规则3需要添零，根据后面的语句是否修改了needZero来检测是否添加0
            chnStr=chnNumChar[0]+chnStr
            logging.debug( "Now:chnStr:"+chnStr)

        #节点内处理
        strIns=SectionToChinese(section)

        #检测当前section的的是否是0，如果是0的话，说明前面没有小节了，已处理完，添加空字符串的节权位就可以
        #否则说明还有小节，需要增加相应层级的节权位
        strIns=strIns+(chnUnitSetion[unitPos] if section != 0 else chnUnitSetion[0])
        #strIns += (section != 0) ? chnUnitSetion[unitPos] : chnUnitSetion[0]
        chnStr=strIns+chnStr
        #当满足小节内的值小于1000且值大于0的时候表示当前小节的千位是一个0，如果前面一小节还有值的时候则添0
        needZero = section < 1000 and section > 0
        num =num/10000
        unitPos=unitPos+1
        logging.debug( "Now:chnStr:"+chnStr)
    return chnStr

def SectionToChinese(section):
    #小节内转换,当前小节内的当前个数的独立计数的权位
    strIns=""
    chnStr=""
    unitPos = 0
    #先设置zero为true，为了规则二，两个相连的0只留一个
    zero = True

    while section > 0:
        v=section % 10
        if v==0:
            #当不是两个0相连的时候或者 添加0在数字中
            if not zero :
                #当出现一个0的时候就设置zero为true，当下一个还是0的时候就不添加0了
                zero = True
                chnStr=chnNumChar[v]+chnStr
        else:
            #当出现一个不是0的数字的时候就设置当前的zero标志为false表示下次遇到0的时候还是要添加
            zero = False
            strIns = chnNumChar[v]
            strIns += chnUnitChar[unitPos]
            #将这个strIns插入到总的字符串的开始的位置
            chnStr=strIns+chnStr

        #权位增加
        unitPos=unitPos+1
        #小节值除以10
        section /= 10

    return chnStr

#主处理方法
def main(num):
    chnStr=""
    if num == 0 :
        chnStr="零"
    else:
        chnStr=NumberToChinese(num)
    logging.info( "result:"+chnStr)



if __name__ == '__main__':
    #设置环境编码
    reload(sys)
    sys.setdefaultencoding('utf8')

    #data = int(sys.argv[1])

    #初始化日志配置
    LOG_FORMAT = "%(asctime)s[%(levelname)s]%(message)s"
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S' 
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    logging.info( "Beginning transfor. ")

    #修改这个数字
    main(120730041)
    logging.info( "transfor over. ")
