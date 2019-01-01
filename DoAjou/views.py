from soynlp.tokenizer import MaxScoreTokenizer
from gensim.models import Word2Vec
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .project2 import Sentence2Vec
from .file import Files

def keyboard(request):
	
    return JsonResponse({
	'type':'buttons',
    'buttons' : ['사용법','시작하기']
	})

@csrf_exempt
def message(request):
        
        message = ((request.body).decode('utf-8'))
        return_json_str = json.loads(message)
        user_name = return_json_str['user_key']
        return_str = return_json_str['content']
        files = Files()
        
        if return_str == "사용법" or return_str == "도움말" :
            return JsonResponse({
                    'message': {
                            'text': "안녕하세요 DoAjou 입니다.\n\
\n* 학식/기식 메뉴 \
\n* 정보통신대학의 교수님\
\n* (소웨/사보/미디어/국디/전자)\
\n* 소프트웨어 학과사무실\
\n* 이메일 / 사무실 / 전화번호 \
\n\t\t물어보세요!"
                    },
                    'keyboard': {
                            'type':'buttons',
                            'buttons' : ['사용법','시작하기']
                    }
            })
        elif return_str == "시작하기" :
            files.file_save(user_name,"0")
            files.file_remove(user_name + "_intend")
            return JsonResponse({
                    'message': {
                            'text': "궁금한 것을 자유롭게 물어보세요!\n※사용법이 궁금하시면 '도움말'을 입력해주세요."
                    },
                    'keyboard': {
                            'type':'text'
                    }
            })
        else :
            model = Sentence2Vec()
            out = model.start(user_name,return_str)
            files.file_save("data_"+user_name,return_str+"\n"+out)
            
            return JsonResponse({
                    'message': {
                            'text': out
                    },
                    'keyboard': {
                            'type': 'text'
                    }
            })
    
