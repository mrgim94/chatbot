# -*- coding: utf-8 -*-



import requests
import json
import urllib2

from PIL import ImageFile
from flask import Flask, request, make_response, jsonify



ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'
URL_OPEN_TIME_OUT = 10



app = Flask(__name__)



#----------------------------------------------------
# 사진 구함
#----------------------------------------------------
def get_photo(answer):

    photo = ''
    index = answer.find('</Photo>')
    
    if index >= 0:
        photo = answer[len('<Photo>'):index]
        answer = answer[index + len('</Photo>'):]
    
    return answer, photo



#----------------------------------------------------
# 사진 크기 구함
#----------------------------------------------------
def get_photo_size(url):

    width = 0
    height = 0
    
    if url == '':
        return width, height
    
    try:
        file = urllib2.urlopen(url, timeout = URL_OPEN_TIME_OUT)
        p = ImageFile.Parser()
        
        while 1:
            data = file.read(1024)
            
            if not data:
                break
            
            p.feed(data)
            
            if p.image:
                width = p.image.size[0]
                height = p.image.size[1]
                break 
        
        file.close()
    except:
        print 'get_photo_size error'
    
    return width, height



#----------------------------------------------------
# 메뉴 구함
#----------------------------------------------------
def get_menu(answer):

    #--------------------------------
    # 메뉴가 있는지 검사
    #--------------------------------
    menu = []
    index = answer.find(' 1. ')
    
    if index < 0:
        return answer, menu
    
    menu_string = answer[index + 1:]
    answer = answer[:index]

    #--------------------------------
    # 메뉴를 배열로 설정
    #--------------------------------
    number = 1
    
    while 1:
        number += 1
        search_string = ' %d. ' % number
        index = menu_string.find(search_string)
        
        if index < 0:
            menu.append(menu_string[3:].strip())
            break;
        
        menu.append(menu_string[3:index].strip())
        menu_string = menu_string[index + 1:]
    
    return answer, menu



#----------------------------------------------------
# 메뉴 버튼 구함
#----------------------------------------------------
def get_menu_button(menu):
    
    if len(menu) == 0:
        return None
    
    menu_button = {
        'type': 'buttons',
        'buttons': menu
    }

    return menu_button



#----------------------------------------------------
# Dialogflow에서 대답 구함
#----------------------------------------------------
def get_answer(text, user_key):
    
    #--------------------------------
    # Dialogflow에 요청
    #--------------------------------
    data_send = { 
        'lang': 'ko',
        'query': text,
        'sessionId': user_key,
        'timezone': 'Asia/Seoul'
    }
    
    data_header = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer adfb4242e4a041...'	# Dialogflow의 Client access token 입력
    }
    
    dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20150910'
    
    res = requests.post(dialogflow_url,
                            data=json.dumps(data_send),
                            headers=data_header)

    #--------------------------------
    # 대답 처리
    #--------------------------------
    if res.status_code != requests.codes.ok:
        return ERROR_MESSAGE
    
    data_receive = res.json()
    answer = data_receive['result']['fulfillment']['speech'] 
    
    return answer



#----------------------------------------------------
# 피자 정보 처리
#----------------------------------------------------
def process_menu_info(menu_name):

    if menu_name == u'라면':
        answer = '<Photo>https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSiwKmEtdnNXQ7JLQDD-sjbezog3s6L7ESyaoQs9UnXnLNL6_SFuQ</Photo>'
        answer += '라면'
    elif menu_name == u'비빔밥':
        answer = '<Photo>https://i.ytimg.com/vi/XyPEZpEo4qc/maxresdefault.jpg</Photo>'
        answer += '비빔밥'
    elif menu_name == u'돈까스':
        answer = '<Photo>https://img.siksinhot.com/place/1351044846469397.jpg</Photo>'
        answer += '돈까스'

    return answer




#----------------------------------------------------
# Dialogflow fullfillment 처리
#----------------------------------------------------
@app.route('/', methods=['POST'])
def webhook():

    #--------------------------------
    # 액션 구함
    #--------------------------------
    req = request.get_json(force=True)
    action = req['result']['action']

    #--------------------------------
    # 액션 처리
    #--------------------------------
    if action == 'menu_info':
        menu_name = req['result']['parameters']['menu_type']
        answer = process_menu_info(menu_name)
    else:
        answer = 'error'

    res = {'speech': answer}
        
    return jsonify(res)



#----------------------------------------------------
# 카카오톡 키보드 처리
#----------------------------------------------------
@app.route("/keyboard")
def keyboard():

    res = {
        'type': 'buttons',
        'buttons': ['대화하기']
    }

    return jsonify(res)



#----------------------------------------------------
# 카카오톡 메시지 처리
#----------------------------------------------------
@app.route('/message', methods=['POST'])
def message():

    #--------------------------------
    # 메시지 받기
    #--------------------------------
    req = request.get_json()
    user_key = req['user_key']
    content = req['content']
    
    if len(user_key) <= 0 or len(content) <= 0:
        answer = ERROR_MESSAGE

    #--------------------------------
    # 답변 구함
    #--------------------------------
    if content == u'대화하기':
        answer = '안녕하세요! 저는 메뉴알려주는 챗봇입니다'
    else:
        answer = get_answer(content, user_key)

    #--------------------------------
    # 사진 구함
    #--------------------------------
    answer, photo = get_photo(answer)
    photo_width, photo_height = get_photo_size(photo)

    #--------------------------------
    # 메뉴 구함
    #--------------------------------
    answer, menu = get_menu(answer)

    #--------------------------------
    # 메시지 설정
    #--------------------------------
    res = {
        'message': {
            'text': answer
        }                    
    }

    #--------------------------------
    # 사진 설정
    #--------------------------------
    if photo != '' and photo_width > 0 and photo_height > 0:
        res['message']['photo'] = {
            'url': photo,
            'width': photo_width,
            'height': photo_height
        }

    #--------------------------------
    # 메뉴 버튼 설정
    #--------------------------------
    menu_button = get_menu_button(menu)
    
    if menu_button != None:
        res['keyboard'] = menu_button 

    return jsonify(res)



#----------------------------------------------------
# 메인 함수
#----------------------------------------------------
if __name__ == '__main__':

    app.run(host='0.0.0.0', port = 5110, threaded=True)    
    
