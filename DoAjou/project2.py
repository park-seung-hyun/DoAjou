#!/usr/bin/python
# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
from soynlp.tokenizer import MaxScoreTokenizer
import numpy as np
from numpy import dot
from numpy.linalg import norm
from bot import *
import pandas as pd
from .file import Files
from .util import Preprocess
import sqlite3

class Sentence2Vec:
    def __init__(self): 
        self.load("ko.bin")
        label = list() 
        label_nt =list()
        scores = {'메일' : 1, '이메일' : 1,'교수님' : 1 , '교수': 0.8,'학식':1,'기식':1,'오늘':0.9,'넘버':0.7,'소웨':0.8,\
         '연락처' : 1, '전화번호' : 1, '번호' : 0.8, '핸드폰' : 1, '휴대폰' : 1, '전화' : 0.8,'전번' : 0.5,\
         '사무실' : 1, '연구실' : 1, '랩실' : 1, '렙실' : 1, '어디':1,'학생식당':1,'기숙사식당':1,'학과사무실':1,'과사':0.8,'과사무실':1.0,'위치':0.8,'소중사':1.0,'소프트웨어중심사업단':1.0}
        tokenizer = MaxScoreTokenizer(scores=scores)
        
        f = open("intend_label.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            line = line.replace("\n","")
            label_nt.append(line)
            b = tokenizer.tokenize(line)
            label.append(b)
        f.close()
        
        self.tokenizer = tokenizer
        self.label = label
        self.label_nt = label_nt
        self.files = Files()
        self.prep = Preprocess()
        
    def load(self, model_file):
        self.model = Word2Vec.load(model_file)

    def get_vector(self, sentence):
        tokenizer = self.tokenizer
        token = tokenizer.tokenize(sentence)
        token = self.prep.replace(token) # data 전처리
        vectors = [self.model.wv[w] for w in token
                   if w in self.model.wv]
        v = np.zeros(self.model.vector_size)

        if (len(vectors) > 0):
            v = (np.array([sum(x) for x in zip(*vectors)])) / v.size

        return v

    def similarity(self, x, y):
        xv = self.get_vector(x)
        yv = self.get_vector(y)

        score = 0
        if yv.all() == 0:
            return 0;
        elif xv.size > 0 and yv.size > 0:
            score = dot(xv, yv) / (norm(xv) * norm(yv))

        return score

    def best_similarity(self,inp):
        temp2 = self.label_nt
        
        h = self.similarity(temp2[0],inp)
        h_index = 0
        for i, value in enumerate(temp2):
            if self.similarity(inp,temp2[i]) > h :
                h = self.similarity(inp,temp2[i])
                h_index = i
        if h_index > 5 and h_index < 12:
            h_index = h_index - 6
        return temp2[h_index],h
    
    def start(self,user_name,inputs):
        
        model = self.model
        inp = self.prep.forword(inputs)
        professor_name =  self.find_pro_name(inp)            
        intend, similarity = self.best_similarity(inp)
        files = self.files
        self.similarity = similarity
        
        if professor_name == "1" :
            answer = "올바른 교수님의 성함을 입력해주세요. (정보통신대학 교수님 한정)"
            files.file_overwrite_save(user_name,"0") # 0 = 교수님 성함 모름.
            return answer
        elif professor_name == "2" :
            answer = "교수님 한분의 성함만 입력해주세요. (정보통신대학 교수님 한정)"
            files.file_overwrite_save(user_name,"0") # 0 = 교수님 성함 모름.
            return answer
        elif professor_name == "제작자" :
            answer = "제작자:\n소프트웨어학과 박승현\n소프트웨어학과 최순원\n소프트웨어학과 김치헌\n DoAjou ver.1.2"
            files.file_overwrite_save(user_name,"0") # 0 = 교수님 성함 모름.
            return answer
        
        if similarity < 0.4 or len(inp) == 1 or intend == self.label_nt[12]:
            if professor_name != "0" and files.file_exist(user_name + "_intend") == True :
                intend = files.file_read(user_name + "_intend").replace("\n","")
                files.file_remove(user_name + "_intend")
            elif professor_name != "0" and files.file_exist(user_name + "_intend") == False :
                files.file_overwrite_save(user_name,professor_name)
                if professor_name == '학과사무실'or professor_name == '소프트웨어중심사업단' :
                        answer = professor_name + "의 어떤 것이 궁금하신가요?\n" + \
                "Q: 사무실/전화번호/이메일"            
                else :
                    answer = professor_name + " 교수님의 어떤 것이 궁금하신가요?\n" + \
                    "Q: 사무실/전화번호/이메일"            
                return answer 
            else:
                files.file_overwrite_save(user_name,"0") # 범위 밖 질문이 들어올 경우 잊음
                answer = "범위 밖 질문입니다."
                files.file_remove(user_name + "_intend")
                return answer
            
        answer = self.find_intend(intend,professor_name,user_name)
        
        return answer
    
    def find_intend(self,intend,professor_name,user_name):
        files = self.files
        
        if intend == self.label_nt[4] :
            answer = self.data_from_db("학식")
            return answer
        elif intend == self.label_nt[5] :
            answer = self.data_from_db("기식")
            return answer
        
        if professor_name == "0" :
            professor_name = files.file_read(user_name).replace("\n","") # 교수 이름이 없을 경우 이전 대화 기록 참조
                        
        if professor_name == "0" :
            user_name = user_name + "_intend"
            if intend == self.label_nt[0]:
                files.file_overwrite_save(user_name,intend)
                answer = "어떤 교수님의 연구실 위치가 궁금하신가요?"
            elif intend == self.label_nt[2]:
                files.file_overwrite_save(user_name,intend)
                answer = "어떤 교수님의 이메일이 궁금하신가요?"
            elif intend == self.label_nt[3]:
                files.file_overwrite_save(user_name,intend)
                answer = "어떤 교수님의 전화번호가 궁금하신가요?"
        else :
            files.file_overwrite_save(user_name,professor_name) # 올바른 교수 이름이 들어올 경우 저장
            if professor_name == '학과사무실' or professor_name == '소프트웨어중심사업단' :
                    final_q = professor_name + ' ' +intend
            else :
                final_q = professor_name+' 교수님 '+ intend
            answer = self.answer(final_q)
            files.file_remove(user_name + "_intend") # 의도 저장파일 삭제
        
        return answer

    def find_pro_name(self, inp):
        name_dic = {'Yenewondim Sinshaw', '강경란', '고영배', '고정길', '김도형',\
           '김동윤','김민구','김성수','김승운','노병희','류기열','변광준',\
           '손경아','안정섭','오상윤','위규범','윤대균','이석원','이정태',\
           '이택균','이환용','임재성','정크리스틴','정태선','조영종',\
           '최경희','최영준','최재영','한경식','황원준','Paul rajib','학과사무실','과사','과사무실',\
                '경란','경란이','영배','정길','정길이','도형','도형이','동윤',\
               '민구','성수','승운','승운이','병희','기열','기열이','광준','광준이',\
               '경아','정섭','정섭이','상윤','상윤이','규범','규범이','대균',\
              '대균이','석원','석원이','정태','택균','택균이','환용','환용이',\
              '정크','정크리','크리스틴','태선','태선이','영종','영종이',\
              '경희','영준','영준이','재영','재영이','경식','경식이','원준',\
              '원준이','예나원딤','에나원딤','yenewondim','Yenewondim',\
              'yenawondim','Yenawondim','라집','폴라집','Paul','폴',\
              'Paulrajib','paulrajib','제작자','소중사','소프트웨어중심사업단',\
               'Ibrahim Mohd Ali Alsofyani','Ran Rong','감동근','구형일','권익진',\
                '김도희','김상배','김상완','김상인','김영길','김영진',\
                '김재현','나상신','박성진','박용배','박익모','선우명훈','양상식',\
                '양회석','오성근','윤원식','이교범','이기근','이상용','이재진',\
                '이정원','이종욱','이채우','이해영','정기현','조성준','조위덕',\
                '조중열','좌동경','지동우','허용석','허준석','홍송남','홍영대',\
                '곽진','김강석','김기형','김상곤','김재훈','손태식','예홍진',\
                '유재희','홍만표','경민호','고욱','김지은','김현희','김효동',\
                '석혜정','신현준','오규환','이경원','이윤진','이주엽','임유상',\
                '장우진','정태영','최정주','구자열','박승규','백호기','이병묵',\
                '이태공','홍성표','란롱'}
        
        name_dic_list = list(name_dic)
        scores_name = {str(name_dic_list[step]) : 1.0 for step, inputs in enumerate(name_dic_list)}
        tokenizer_name = MaxScoreTokenizer(scores=scores_name)
        c = tokenizer_name.tokenize(inp)
        c = self.prep.replace(c)
        professor_name = "0" # 초기값
        check = 0
        for step, inputs in enumerate(name_dic):
            for i in range(len(c)):
                if c[i] == inputs:
                    professor_name = inputs
                    check = check + 1
        c = self.tokenizer.tokenize(inp)            
        if professor_name == "0" :
            for i in range(len(c)):
                if self.find_extra_name(c[i])==True:
                    professor_name = "1"
                    break;
        # 교수님 성함이 두명 이상인 경우
        if check > 1 :            
            professor_name = "2" # 2명 이상의 교수

        return professor_name
    
    def find_extra_name(self, token):
        lastname_dic = {'김','이','박','최','정','강','조','윤','장','임','한',\
                        '오','서','권','황','안','송','홍','류','유','손','차','구','부'}
        if len(token) == 3 and self.model.wv.vocab.get(token) == None:
            for step, inputs in enumerate(lastname_dic):
                if token[0] == inputs:
                    return True
        return False
    
    def answer(self, string):
        kv = pd.read_csv('key_value.csv', encoding='CP949')
        answer = string      
        for step,value in enumerate(kv.key):    
            value = value.replace("\n","")
            if value == string:
                answer = kv.value[step]
                break
#         if answer == string :
#             answer = "올바른 질문을 입력해주세요!"
        return answer
    
    def data_from_db(self, rest): # rest = 레스토랑

        con = sqlite3.connect("meal.db")
        cur = con.cursor()

        if rest == '학식':
            query = ("SELECT Haksik FROM meal")
        if rest == '기식':
            query = ("SELECT Gisik FROM meal")

        cur.execute(query)
        data = cur.fetchone()
        
        query = ("SELECT Date FROM meal")
        cur.execute(query)
        date_data = cur.fetchone()
        
        return date_data[0] + data[0]