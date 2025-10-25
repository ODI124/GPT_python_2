import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
import speech_recognition as sr
import pyttsx3
import datetime

class VoiceAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
    def initUI(self):
        self.setWindowTitle('음성 인식 프로그램')
        self.setGeometry(100, 100, 400, 300)
        
        # 중앙 위젯 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 레이아웃 설정
        layout = QVBoxLayout(central_widget)
        
        # 텍스트 출력 영역
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        
        # 음성인식 버튼
        self.voice_button = QPushButton('음성인식')
        self.voice_button.clicked.connect(self.recognize_speech)
        layout.addWidget(self.voice_button)
        
    def recognize_speech(self):
        try:
            with sr.Microphone() as source:
                self.text_edit.append("음성을 인식하고 있습니다...")
                audio = self.recognizer.listen(source, timeout=5)
                
            text = self.recognizer.recognize_google(audio, language='ko-KR')
            self.text_edit.append(f"인식된 음성: {text}")
            
            # 시간을 물어보는 경우 처리
            if "시간" in text:
                current_time = datetime.datetime.now().strftime("%H시 %M분")
                response = f"현재 시간은 {current_time} 입니다."
                self.text_edit.append(f"응답: {response}")
                self.speak(response)
            
        except sr.UnknownValueError:
            self.text_edit.append("음성을 인식하지 못했습니다.")
        except sr.RequestError:
            self.text_edit.append("음성 인식 서비스에 접근할 수 없습니다.")
        except Exception as e:
            self.text_edit.append(f"오류 발생: {str(e)}")
    
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VoiceAssistant()
    window.show()
    sys.exit(app.exec_())
