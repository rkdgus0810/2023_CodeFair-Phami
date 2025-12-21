import speech_recognition as sr
import time
import datetime
import openai
import os
from gtts import gTTS
import socket
from _thread import *

HOST = '10.46.68.130' ## server에 출력되는 ip를 입력해주세요 ##
PORT = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        data=data.decode()
        print("recive : ",data)
        if data=="타이레놀":
            print("타이레놀")

start_new_thread(recv_data, (client_socket,))
print('>> Connect Server')


openai.api_key = "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"
def gpt(i_message:str):
    prompt = i_message
    response = (openai.Completion()).create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            best_of=1,)
    gpt_message=response.choices[0].text.strip()
    return gpt_message
def diff_message(message1:str, message2:str):
    gpt_input="\"{}\"와 \"{}\"는 같은 의미야?".format(message1,message2)
    gpt_message=gpt(gpt_input)
    print(gpt_message)
    print(gpt_message[0])
    if gpt_message[0]=='네':
        print("두 말은 의미가 똑같습니다.")
        return True
    elif gpt_message[0]=='아' and gpt_message[1]=='니' and gpt_message[2]=='요':
        print("두 말은 의미가 똑같습니다.")
        return False
    else:
        return "error"


def log_print(l_message:str):
    time=datetime.datetime.now()
    log_message=str(time)+">> "+l_message
    print(log_message)

def speak(text, lang="ko",speed=False):
    tts = gTTS(text=text,lang=lang)
    tts.save('message.mp3')
    os.system("mpg123 message.mp3")
ok=0
try:
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            log_print('recording..')
            audio = r.listen(source,timeout=3)
            print("record complete!")
            try:
                recog_message=r.recognize_google(audio,language='ko-KR')
                log_print('record result : ' + recog_message)
                time.sleep(1)
                if recog_message=="파미야" or recog_message=="밤이야" or recog_message=="바미야" or recog_message=="타미야":
                    speak("네! 무엇을 도와드릴 까요?")
                    ok=1
                    break
            except sr.UnknownValueError:
                log_print('I can''t understand the speech.')
            except sr.RequestError as e:
                log_print(f'An error has occurred. Causes of the error : error {e}')
except KeyboardInterrupt:
    pass
if ok==1:
    os.system("clear")
    log_print("recog <phami> success!!")
    log_print("recording...(How can I help you?)")
    try:
        r=sr.Recognizer()
        with sr.Microphone() as source:
            log_print('recording..')
            audio=r.listen(source,timeout=3)
            log_print("record complete!")
            try:
                recog_message=r.recognize_google(audio,language='ko-KR')
                log_print('record result: '+recog_message)
                diff_result=diff_message("이 약은 무슨 약이야?",recog_message)
                if diff_result== True:
                    socket_message="run"
                    client_socket.send(socket_message.encode())
                    print("메시지 보냄")
                else:
                    message=gpt(recog_message)
                    speak(message)
                    time.sleep(1)        
            except sr.UnknownValueError:
                log_print('I can''t understand the speech.')
            except sr.RequestError as e:
                log_print(f'An error has occurred. Causes of the error : error {e}')
    except KeyboardInterrupt:
        pass
