import requests
import os, signal

from flask import Flask
from flask import request
from flask import Response
import openai

openai.api_key = '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'

TOKEN = "6576063747:AAFyFSbw1s4vfVuaBwODrw2wssJtfFGGTkA"

app = Flask(__name__)


def parse_message(message):
    print("message-->",message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("Text :", txt)
    return chat_id,txt
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    response = requests.post(url,json=payload)
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
       
        chat_id,txt = parse_message(msg)
        
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": txt}]
            )
        response = completion['choices'][0]['message']['content']
        print("ChatGPT response: ",response) 
        tel_send_message(chat_id,response)
        process()
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(debug=True)