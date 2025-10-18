import os
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
import mysql.connector
from winotify import Notification
import pygame
from mutagen import File as MutagenFile
import ttkbootstrap as tb

# ---------------- 환경설정 ----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'aloha',
    'password': '123456',
    'database': 'alarmdb',
    'port': 3306
}
ALARM_DIR = r"C:\alarm"
DEFAULT_SOUND = os.path.join(ALARM_DIR, "기본.mp3")
os.makedirs(ALARM_DIR, exist_ok=True)

# ---------- DB 초기화 ----------
def init_db():
    tmp = DB_CONFIG.copy()
    dbname = tmp.pop('database')
    conn = mysql.connector.connect(**tmp)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4;")
    conn.commit()
    cur.close()
    conn.close()

    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS alarm (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        alarm_time DATETIME,
        sound_path VARCHAR(1024)
    );''')
    conn.commit()
    cur.close()
    conn.close()

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def fetch_alarms():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM alarm ORDER BY alarm_time ASC")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def insert_alarm(name, alarm_time, sound_path):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO alarm (name, alarm_time, sound_path) VALUES (%s,%s,%s)",
                (name, alarm_time, sound_path))
    conn.commit()
    cur.close()
    conn.close()

def delete_alarm_db(aid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM alarm WHERE id=%s", (aid,))
    conn.commit()
    cur.close()
    conn.close()

# ---------- 알람 재생 ----------
class AlarmPlayer(threading.Thread):
    def __init__(self, path, stop_event):
        super().__init__(daemon=True)
        self.path = path
        self.stop_event = stop_event

    def run(self):
        try:
            pygame.mixer.init()
            length = MutagenFile(self.path).info.length if os.path.exists(self.path) else 5
            while not self.stop_event.is_set():
                if not os.path.exists(self.path):
                    return
                pygame.mixer.music.load(self.path)
                pygame.mixer.music.play()
                time.sleep(length)
        except:
            pass

# ---------- 메인 앱 ----------
class AlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⏰ 심플 알람")
        self.root.geometry("500x350")
        self.running_alarms = {}
        init_db()
        self.build_ui()
        threading.Thread(target=self.scheduler, daemon=True).start()

    def build_ui(self):
        top = ttk.Frame(self.root)
        top.pack(fill="x", pady=5)
        ttk.Label(top, text="알람 리스트", font=("맑은 고딕", 14)).pack(side="left")
        ttk.Button(top, text="＋ 추가", command=self.open_add).pack(side="right")

        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh()

    def refresh(self):
        for w in self.frame.winfo_children():
            w.destroy()
        for a in fetch_alarms():
            card = ttk.Frame(self.frame, padding=5, relief="raised")
            card.pack(fill="x", pady=2)
            ttk.Label(card, text=f"{a['name']}  -  {a['alarm_time']}").pack(side="left")
            ttk.Button(card, text="삭제", command=lambda aid=a['id']: self.delete_alarm(aid)).pack(side="right")

    def delete_alarm(self, aid):
        if messagebox.askyesno("삭제", "삭제하시겠습니까?"):
            delete_alarm_db(aid)
            self.refresh()

    def open_add(self):
        AddAlarmWindow(self)

    def scheduler(self):
        while True:
            now = datetime.now()
            for a in fetch_alarms():
                at = datetime.fromisoformat(a['alarm_time']) if isinstance(a['alarm_time'], str) else a['alarm_time']
                if 0 <= (at - now).total_seconds() < 1 and a['id'] not in self.running_alarms:
                    self.trigger_alarm(a)
            time.sleep(0.5)

    def trigger_alarm(self, alarm):
        Notification(app_id="AlarmApp", title=f"{alarm['name']}", msg=f"{alarm['alarm_time']}").show()
        stop_event = threading.Event()
        AlarmPlayer(alarm['sound_path'] or DEFAULT_SOUND, stop_event).start()
        self.running_alarms[alarm['id']] = stop_event

# ---------- 알람 추가 창 ----------
class AddAlarmWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.title("알람 추가")
        self.geometry("300x200")
        self.name_var = tk.StringVar()
        self.sound_var = tk.StringVar(value=DEFAULT_SOUND)

        tk.Label(self, text="알람 이름").pack()
        tk.Entry(self, textvariable=self.name_var).pack()

        tk.Label(self, text="시간 선택 (오늘)").pack()
        f = tk.Frame(self)
        f.pack()
        now = datetime.now()
        self.hour_cb = ttk.Combobox(f, values=[f"{i:02d}" for i in range(24)], width=3)
        self.min_cb = ttk.Combobox(f, values=[f"{i:02d}" for i in range(60)], width=3)
        self.sec_cb = ttk.Combobox(f, values=[f"{i:02d}" for i in range(60)], width=3)
        self.hour_cb.set(f"{now.hour:02d}")
        self.min_cb.set(f"{now.minute:02d}")
        self.sec_cb.set(f"{now.second:02d}")
        self.hour_cb.pack(side="left"); self.min_cb.pack(side="left"); self.sec_cb.pack(side="left")

        tk.Button(self, text="소리 선택", command=self.choose_sound).pack(pady=5)
        tk.Button(self, text="저장", command=self.save).pack(pady=5)

    def choose_sound(self):
        path = filedialog.askopenfilename(filetypes=[("MP3 파일","*.mp3")])
        if path: self.sound_var.set(path)

    def save(self):
        name = self.name_var.get()
        if not name: messagebox.showwarning("입력", "이름을 입력하세요."); return
        h, m, s = int(self.hour_cb.get()), int(self.min_cb.get()), int(self.sec_cb.get())
        dt = datetime.now().replace(hour=h, minute=m, second=s, microsecond=0)
        if dt < datetime.now(): dt += timedelta(days=1)  # 과거 시간이면 다음 날로 설정
        insert_alarm(name, dt, self.sound_var.get())
        self.app.refresh()
        self.destroy()

# ---------- 실행 ----------
if __name__ == "__main__":
    root = tb.Window(themename="cyborg")
    app = AlarmApp(root)
    root.mainloop()

