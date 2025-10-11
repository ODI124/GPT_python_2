import tkinter as tk
from tkinter import messagebox, filedialog
from gtts import gTTS
import datetime
import os

def save_audio():
    text = text_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("경고", "텍스트를 입력해주세요.")
        return

    # 파일 기본 이름 생성
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename_text = text[:10].replace(" ", "")
    default_filename = f"{timestamp}_{filename_text}.mp3"

    # 저장할 위치 및 파일명 선택
    file_path = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3 파일", "*.mp3")],
        initialfile=default_filename,
        title="음성 파일 저장 위치 선택"
    )

    if not file_path:
        return  # 사용자가 취소한 경우

    try:
        tts = gTTS(text=text, lang='ko')
        tts.save(file_path)
        messagebox.showinfo("성공", f"음성 파일이 저장되었습니다:\n{file_path}")
    except Exception as e:
        messagebox.showerror("오류", f"음성 변환에 실패했습니다:\n{e}")

# GUI 설정
app = tk.Tk()
app.title("텍스트 음성 변환기")
app.geometry("500x300")

tk.Label(app, text="텍스트 입력", font=("Arial", 12)).pack(pady=5)
text_entry = tk.Text(app, height=10, width=60)
text_entry.pack(padx=10)

save_btn = tk.Button(app, text="음성 변환 및 저장", command=save_audio)
save_btn.pack(pady=10)

app.mainloop()
