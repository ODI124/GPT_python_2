import os
import time
import wave
import pyaudio
import threading
import queue
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from faster_whisper import WhisperModel
from googletrans import Translator

# 환경 변수 설정
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 오디오 큐 생성
audio_queue = queue.Queue()

class TranscriptionWorker(QObject):
    # 트랜스크립션 결과를 UI에 전달할 시그널
    transcription_signal = pyqtSignal(str, str)

    def __init__(self, model, audio_queue):
        super().__init__()
        self.model = model
        self.audio_queue = audio_queue
        self.is_running = True
        self.translator = Translator()

    def run(self):
        while self.is_running:
            try:
                # 큐에서 오디오 파일 경로 가져오기
                file_path = self.audio_queue.get(timeout=1)
                transcription = self.transcribe_chunk(file_path)
                translated_text = self.translate_text(transcription)
                self.transcription_signal.emit(transcription, translated_text)
                os.remove(file_path)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"TranscriptionWorker error: {e}")

    def transcribe_chunk(self, file_path):
      segments, info = self.model.transcribe(file_path, beam_size=3)
      transcription = ''.join(segment.text for segment in segments)
      
      # info[0]이 언어 코드('ko')일 수 있으므로, 코드를 수정합니다.
      confidence_threshold = 0.4
      confidence = float(info[1])  # 두 번째 항목을 신뢰도로 사용
      if confidence < confidence_threshold:
          print(f"Low confidence transcription: {confidence}")
          return ""
      
      return transcription

    def translate_text(self, text):
        try:
            translated = self.translator.translate(text, dest='en')
            return translated.text
        except Exception as e:
            print(f"Translation error: {e}")
            return "Translation Error"

    def stop(self):
        self.is_running = False

class VoiceRecognitionApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # main.ui 파일을 로드
        uic.loadUi("main.ui", self)

        # 하단 고정 상태 변수 추가
        self.is_fixed_bottom = False

        # Translator 인스턴스 생성
        self.translator = Translator()

        # 아이콘 설정을 위한 이미지 경로
        self.start_icon_path = "start_icon.png"
        self.pause_icon_path = "pause_icon.png"  # pause 아이콘 경로 추가
        self.stop_icon_path = "stop_icon.png"
        self.fixed_bottom_icon_path = "fixed_bottom_icon.png"  # 하단 고정 아이콘 경로
        self.restore_icon_path = "restore_icon.png"  # 복원 아이콘 경로

        # 아이콘 설정
        self.start_button = QtWidgets.QPushButton()
        self.start_button.setIcon(QtGui.QIcon(self.start_icon_path))
        self.pause_button = QtWidgets.QPushButton()  # pause 버튼 추가
        self.pause_button.setIcon(QtGui.QIcon(self.pause_icon_path))
        self.stop_button = QtWidgets.QPushButton()
        self.stop_button.setIcon(QtGui.QIcon(self.stop_icon_path))
        self.fixed_bottom_button = QtWidgets.QPushButton()  # 하단 고정 버튼 추가
        self.fixed_bottom_button.setIcon(QtGui.QIcon(self.fixed_bottom_icon_path))

        # 버튼 크기 조정
        self.start_button.setIconSize(QtCore.QSize(40, 40))
        self.pause_button.setIconSize(QtCore.QSize(40, 40))  # pause 버튼 크기 조정
        self.stop_button.setIconSize(QtCore.QSize(40, 40))
        self.fixed_bottom_button.setIconSize(QtCore.QSize(40, 40))

        # horizontalLayout을 좌측 정렬
        self.horizontalLayout.addWidget(self.start_button)
        self.horizontalLayout.addWidget(self.pause_button)
        self.horizontalLayout.addWidget(self.stop_button)
        self.horizontalLayout.addWidget(self.fixed_bottom_button)  # 하단 고정 버튼 추가
        self.horizontalLayout.setAlignment(Qt.AlignLeft)

        # verticalLayout에 텍스트 출력 라벨 추가
        self.transcription_label_1 = QtWidgets.QLabel("알클 보이스", self)
        self.transcription_label_2 = QtWidgets.QLabel("", self)
        self.verticalLayout.addWidget(self.transcription_label_1)
        self.verticalLayout.addWidget(self.transcription_label_2)

        # UI 스타일 설정 (투명 배경, 흰색 텍스트)
        # 창 테두리 제거
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 창 배경 투명하게
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.container.setStyleSheet("background-color: transparent;")

        # 미니 모드로 시작
        self.mini_mode()

        # 버튼 스타일        
        self.start_button.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);")
        self.pause_button.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);")
        self.stop_button.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);")
        self.fixed_bottom_button.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);")  # 하단 고정 버튼 스타일

        # 음성 인식 관련 설정
        self.is_running = False
        self.is_paused = False  # 일시정지 상태를 위한 변수 추가
        self.model = WhisperModel("large-v3", device="cuda", compute_type="float16")
        self.transcriptions = ["", ""]
        self.p = pyaudio.PyAudio()
        self.stream = None

        # Transcription 스레드 설정
        self.transcription_worker = TranscriptionWorker(self.model, audio_queue)
        self.transcription_thread = QtCore.QThread()
        self.transcription_worker.moveToThread(self.transcription_thread)
        self.transcription_worker.transcription_signal.connect(self.update_transcription)
        self.transcription_thread.started.connect(self.transcription_worker.run)
        self.transcription_thread.start()

        # 버튼 클릭 이벤트 연결
        self.start_button.clicked.connect(self.start_recognition)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.stop_button.clicked.connect(self.exit_program)
        self.fixed_bottom_button.clicked.connect(self.toggle_fixed_bottom)  # 하단 고정 버튼 이벤트 연결

        # 마우스 드래그로 창 이동을 위한 변수
        self.is_dragging = False
        self.drag_start_position = QtCore.QPoint()

    def toggle_fixed_bottom(self):
        # 하단 고정 기능 토글
        self.is_fixed_bottom = not self.is_fixed_bottom
        if self.is_fixed_bottom:
            self.bottom_mode()
        else:
            self.mini_mode()

    def mini_mode(self):
        # icon 토글
        self.fixed_bottom_button.setIcon(QtGui.QIcon(self.fixed_bottom_icon_path))

        # 프레임의 가로 사이즈를 전체 화면에 맞게 조정
        self.setFixedWidth(800)
        self.container.setFixedWidth(800)

        # 스타일 조정 및 라벨 크기 설정
        self.transcription_label_1.setFixedWidth(600)  # 라벨 가로 크기 설정 600
        self.transcription_label_2.setFixedWidth(600)  # 라벨 가로 크기 설정 600
        self.transcription_label_1.setFixedHeight(60)
        self.transcription_label_2.setFixedHeight(50)
        # 수직 레이아웃을 프레임의 중앙에 위치시키기 위한 정렬 설정
        self.container.setLayout(self.verticalLayout)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)  # 수직 레이아웃의 정렬을 가운데로 설정

        # verticalLayout의 하단 마진을 50으로 설정
        self.verticalLayout.setContentsMargins(0, 0, 0, 50)

        # QLabel 글씨 크기, 색상, 정렬 및 줄바꿈 설정
        self.transcription_label_1.setStyleSheet("""
            padding: 10px; 
            color: white; 
            font-size: 20px; 
            background-color: rgba(0, 0, 0, 0.5);
        """)
        self.transcription_label_1.setWordWrap(True)  # 자동 줄바꿈
        self.transcription_label_1.setAlignment(Qt.AlignCenter)  # 가운데 정렬

        self.transcription_label_2.setStyleSheet("""
            padding: 10px; 
            color: white; 
            font-size: 16px; 
            background-color: rgba(0, 0, 0, 0.5);
        """)
        self.transcription_label_2.setWordWrap(True)  # 자동 줄바꿈
        self.transcription_label_2.setAlignment(Qt.AlignCenter)  # 가운데 정렬

    def bottom_mode(self):
        # icon 토글
        self.fixed_bottom_button.setIcon(QtGui.QIcon(self.restore_icon_path))

        # 창을 화면 하단에 고정하는 기능
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry()
        window_height = self.height()
        self.move(0, screen_geometry.height() - window_height)  # 화면 하단으로 이동

        # 프레임의 가로 사이즈를 전체 화면에 맞게 조정
        self.setFixedWidth(screen_geometry.width())
        self.container.setFixedWidth(screen_geometry.width())

        # 하단 고정 모드 스타일 조정 및 라벨 크기 설정
        self.transcription_label_1.setFixedWidth(int(screen_geometry.width() * 0.8))  # 라벨 가로 크기 설정 80%
        self.transcription_label_1.setFixedHeight(120)
        self.transcription_label_1.setStyleSheet("""
            padding: 10px; 
            color: white; 
            font-size: 40px; 
            background-color: rgba(0, 0, 0, 0.5);
        """)  # 글씨 크기 조정

        self.transcription_label_2.setFixedWidth(int(screen_geometry.width() * 0.8))  # 라벨 가로 크기 설정 80%
        self.transcription_label_2.setFixedHeight(100)
        self.transcription_label_2.setStyleSheet("""
            padding: 10px; 
            color: white; 
            font-size: 36px; 
            background-color: rgba(0, 0, 0, 0.5);
        """)  # 글씨 크기 조정

        # 수직 레이아웃을 프레임의 중앙에 위치시키기 위한 정렬 설정
        self.container.setLayout(self.verticalLayout)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)  # 수직 레이아웃의 정렬을 가운데로 설정
        # self.verticalLayout.setSpacing(80) 
        

        # verticalLayout의 하단 마진을 200으로 설정
        self.verticalLayout.setContentsMargins(0, 0, 0, 200)

    def toggle_pause(self):
        if self.is_running:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.pause_button.setText("재개")  # 버튼 텍스트 변경
                self.pause_button.setStyleSheet("background-color: rgba(255, 0, 0, 0.2);")  # pause 상태 시 빨간색으로
            else:
                self.pause_button.setText("일시정지")  # 버튼 텍스트 변경
                self.pause_button.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);")  # resume 상태 시 원래 색으로

    def start_recognition(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.pause_button.setText("일시정지")
            self.pause_button.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);")
            self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
            self.thread = threading.Thread(target=self.run_recognition)
            self.thread.start()

    def stop_recognition(self):
        self.is_running = False
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()

    def exit_program(self):
        # 프로그램 종료
        self.is_running = False
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        # Transcription 스레드 종료
        self.transcription_worker.stop()
        self.transcription_thread.quit()
        self.transcription_thread.wait()
        QtCore.QCoreApplication.quit()

    def run_recognition(self):
        while self.is_running:
            if self.is_paused:
                time.sleep(0.1)
                continue
            chunk_file = f"temp_{int(time.time()*1000)}.wav"  # 고유한 파일명 생성
            self.record_chunk(self.p, self.stream, chunk_file, chunk_length=4)
            audio_queue.put(chunk_file)

    def record_chunk(self, p, stream, file_path, chunk_length=5):
        frames = []
        for _ in range(0, int(16000 / 1024 * chunk_length)):
            data = stream.read(1024)
            frames.append(data)

        wf = wave.open(file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))
        wf.close()

    def update_transcription(self, transcription, translated_text):
        # 최근 2개의 트랜스크립션을 업데이트
        self.transcriptions = [transcription] + self.transcriptions[:1]

        # UI 업데이트
        self.transcription_label_1.setText(self.transcriptions[0])
        self.transcription_label_2.setText(self.transcriptions[1])

        # 로그 파일에 저장 (선택사항)
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(transcription + "\n")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            event.accept()

    def closeEvent(self, event):
        # 창이 닫힐 때 리소스 정리
        self.exit_program()
        event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = VoiceRecognitionApp()

    # 항상 위에 고정 설정
    window.setWindowFlags(window.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
    window.show()
    window.raise_()  # 창을 가장 위로 가져옴

    sys.exit(app.exec_())
