import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import os
import subprocess
from plyer import notification

# 초기화
engine = pyttsx3.init()
recognizer = sr.Recognizer()
MIC_INDEX = None  # 기본 마이크 장치

# 음성 출력
def speak(text):
    engine.say(text)
    engine.runAndWait()

# 음성 입력
def listen():
    try:
        with sr.Microphone(device_index=MIC_INDEX) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        return recognizer.recognize_google(audio, language='ko-KR')
    except:
        return ""

# 기능 정의
def tell_time():
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    notification.notify(title="현재 시간", message=time_str)
    speak(f"현재 시간은 {now.hour}시 {now.minute}분 입니다")
    text_output.insert(tk.END, f"시간: {time_str}\n")

def search_google():
    speak("무엇을 검색할까요?")
    text_output.insert(tk.END, "무엇을 검색할까요?\n")
    query = listen()
    text_output.insert(tk.END, f"검색어: {query}\n")
    if query:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"{query} 검색 결과입니다.")

def open_website(keyword):
    urls = {'구글':'https://www.google.com','유튜브':'https://www.youtube.com','GPT':'https://chat.openai.com'}
    if keyword in urls:
        webbrowser.open(urls[keyword])
        speak(f"{keyword} 사이트를 실행합니다.")
        text_output.insert(tk.END, f"사이트 실행: {keyword}\n")

def run_program(keyword):
    programs = {'ZOOM':'C:/Users/USERNAME/AppData/Roaming/Zoom/bin/Zoom.exe','VS CODE':'C:/Users/USERNAME/AppData/Local/Programs/Microsoft VS Code/Code.exe'}
    if keyword in programs:
        subprocess.Popen(programs[keyword])
        speak(f"{keyword} 프로그램을 실행합니다.")
        text_output.insert(tk.END, f"프로그램 실행: {keyword}\n")

def close_program(keyword):
    apps = {'크롬':'chrome','ZOOM':'Zoom','VS CODE':'Code'}
    if keyword in apps:
        os.system(f"taskkill /im {apps[keyword]}.exe /f")
        speak(f"{keyword} 프로그램을 종료합니다.")
        text_output.insert(tk.END, f"프로그램 종료: {keyword}\n")

def save_memo():
    speak("메모할 내용을 말씀해주세요.")
    text_output.insert(tk.END, "메모할 내용을 말씀해주세요.\n")
    memo_text = listen()
    text_output.insert(tk.END, f"메모 내용: {memo_text}\n")
    if memo_text:
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_memo.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(memo_text)
        speak("메모가 저장되었습니다.")

def execute_command():
    command = listen()
    text_output.insert(tk.END, f"음성 명령: {command}\n")
    if '시간' in command:
        tell_time()
    elif '검색' in command:
        search_google()
    elif '메모' in command:
        save_memo()
    elif '종료' in command:
        for app in ['크롬','ZOOM','VS CODE']:
            if app in command:
                close_program(app)
    elif '앱 종류' in command:
        speak("비서 프로그램을 종료합니다.")
        root.destroy()
    else:
        for site in ['구글','유튜브','GPT']:
            if site in command:
                open_website(site)
                return
        for prog in ['ZOOM','VS CODE']:
            if prog in command:
                run_program(prog)
                return
        speak("알 수 없는 명령입니다.")
        text_output.insert(tk.END, "알 수 없는 명령입니다.\n")

# GUI 생성
root = tk.Tk()
root.title("파이썬 음성 비서")
root.geometry("600x500")
root.resizable(False, False)

# 타이틀 프레임
frame_title = tk.Frame(root, bd=2, relief='raised')
frame_title.pack(fill='x', pady=5)
label = tk.Label(frame_title, text="📢 파이썬 음성 비서", font=("Arial", 16, 'bold'))
label.pack(padx=10, pady=5)

# 명령 버튼 프레임
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

button_execute = tk.Button(frame_buttons, text="🎙 음성 명령 실행", command=execute_command, font=("Arial", 12), bg='#A8E6CF', fg='black', width=20, height=2)
button_execute.grid(row=0, column=0, padx=10, pady=5)

button_search = tk.Button(frame_buttons, text="🔍 검색", command=search_google, font=("Arial", 12), bg='#B3E5FC', fg='black', width=20, height=2)
button_search.grid(row=0, column=1, padx=10, pady=5)

button_memo = tk.Button(frame_buttons, text="📝 메모", command=save_memo, font=("Arial", 12), bg='#FFE0B2', fg='black', width=20, height=2)
button_memo.grid(row=1, column=0, padx=10, pady=5)

button_time = tk.Button(frame_buttons, text="⏰ 시간 확인", command=tell_time, font=("Arial", 12), bg='#D1C4E9', fg='black', width=20, height=2)
button_time.grid(row=1, column=1, padx=10, pady=5)

# 출력 프레임
frame_output = tk.Frame(root)
frame_output.pack(pady=10)

text_output = scrolledtext.ScrolledText(frame_output, width=70, height=20, font=("Arial", 10))
text_output.pack()

root.mainloop()