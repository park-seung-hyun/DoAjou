#!/usr/bin/python
# -*- coding: utf-8 -*-
from soynlp.normalizer import *

class Preprocess:
    def __init__(self):
        pass
    
    def forword(self, str_line):
        line = only_hangle(str_line)
        line = line.replace(" ","")
        return line
    
    def replace(self, word_list) :
        dic = {'넘버':'번호','경란':'강경란','경란이':'강경란','영배':'고영배','정길':'고정길',\
               '정길이':'고정길','도형':'김도형','도형이':'김도형','동윤':'김동윤',\
               '민구':'김민구','성수':'김성수','승운':'김승운','승운이':'김승운','병희':'노병희',\
              '기열':'류기열','기열이':'류기열','광준':'변광준','광준이':'변광준',\
               '경아':'손경아','정섭':'안정섭','정섭이':'안정섭','상윤':'오상윤',\
              '상윤이':'오상윤','규범':'위규범','규범이':'위규범','대균':'윤대균',\
              '대균이':'윤대균','석원':'이석원','석원이':'이석원','정태':'이정태',\
              '택균':'이택균','택균이':'이택균','환용':'이환용','환용이':'이환용',\
              '정크':'정크리스틴','정크리':'정크리스틴','크리스틴':'정크리스틴',\
              '태선':'정태선','태선이':'정태선','영종':'조영종','영종이':'조영종',\
              '경희':'최경희','영준':'최영준','영준이':'최영준','재영':'최재영',\
              '재영이':'최재영','경식':'한경식','경식이':'한경식','원준':'황원준',\
              '원준이':'황원준','예나원딤':'Yenewondim Sinshaw','에나원딤':'Yenewondim Sinshaw',\
              'yenewondim':'Yenewondim Sinshaw','Yenewondim':'Yenewondim Sinshaw',\
              'yenawondim':'Yenewondim Sinshaw','Yenawondim':'Yenewondim Sinshaw',\
              '연구실':'사무실','랩실':'사무실','렙실':'사무실','이멜':'이메일','전번':'전화번호',\
              '라집':'Paul rajib','폴라집':'Paul rajib','Paul':'Paul rajib','폴':'Paul rajib',\
              'Paulrajib':'Paul rajib','paulrajib':'Paul rajib','학생식당':'학식','기숙사식당':'기식',\
              '과사':'학과사무실','과사무실':'학과사무실','메뉴':'','점':'','은':'','도':'',\
              '오늘':'','소웨':'','소중사':'소프트웨어중심사업단','란롱':'Ran Rong'}

        for step,value in enumerate(word_list):
            if value in dic :
                word_list[step] = dic.get(value)
        return word_list
    
    