# QR 코드 생성 및 관리 GUI 프로그램
# 언어: Python 3.13
# GUI: tkinter
# QR 코드 생성: qrcode
# DB: mysql-connector-python

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
import os
import uuid
from datetime import datetime
import mysql.connector

# DB 연결 설정
# 사용자: python, 비밀번호: 123456
# DB 이름은 기존과 동일하게 사용 (qr_code)
db_config = {
    'host': 'localhost',
    'user': 'python',
    'password': '123456',
    'database': 'python'
}

# DB 연결 함수
def get_connection():
    return mysql.connector.connect(**db_config)

# 테이블 생성 함수 (QR 코드 테이블이 없을 경우 생성)
def create_table_if_not_exists():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qr_code (
            no INT AUTO_INCREMENT PRIMARY KEY,
            id VARCHAR(36) NOT NULL,
            name VARCHAR(100) NOT NULL,
            value TEXT NOT NULL,
            path TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# 프로그램 시작 시 테이블 확인 및 생성
create_table_if_not_exists()



# QR 코드 저장 함수
def save_qr_to_db(qr_id, name, value, path):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("""
        INSERT INTO qr_code (id, name, value, path, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (qr_id, name, value, path, now, now))
    conn.commit()
    cursor.close()
    conn.close()

# QR 코드 수정 함수
def update_qr_name(qr_no, new_name):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("""
        UPDATE qr_code SET name=%s, updated_at=%s WHERE no=%s
    """, (new_name, now, qr_no))
    conn.commit()
    cursor.close()
    conn.close()

# QR 코드 삭제 함수
def delete_qr(qr_no):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM qr_code WHERE no=%s", (qr_no,))
    result = cursor.fetchone()
    if result:
        try:
            os.remove(result[0])
        except:
            pass
    cursor.execute("DELETE FROM qr_code WHERE no=%s", (qr_no,))
    conn.commit()
    cursor.close()
    conn.close()

# QR 코드 생성 함수
def generate_qr():
    name = entry_name.get()
    value = entry_value.get()
    folder = entry_path.get()

    if not (name and value and folder):
        messagebox.showerror("입력 오류", "모든 필드를 입력해주세요.")
        return

    qr_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{name}.png"
    full_path = os.path.join(folder, filename)

    img = qrcode.make(value)
    img.save(full_path)

    save_qr_to_db(qr_id, name, value, full_path)
    messagebox.showinfo("완료", f"QR 코드가 저장되었습니다: {full_path}")
    refresh_dashboard()

# 대시보드 갱신
def refresh_dashboard():
    for row in tree.get_children():
        tree.delete(row)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT no, name, value, path FROM qr_code")
    for (no, name, value, path) in cursor.fetchall():
        tree.insert('', 'end', values=(no, name, value, path))
    cursor.close()
    conn.close()

# 선택된 항목에서 수정
def on_edit():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("선택 없음", "수정할 QR 코드를 선택하세요.")
        return
    values = tree.item(selected, 'values')
    qr_no = values[0]

    new_name = simple_input("QR 코드 이름 수정", "새 이름을 입력하세요:", values[1])
    if new_name:
        update_qr_name(qr_no, new_name)
        refresh_dashboard()

# 선택된 항목 삭제
def on_delete():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("선택 없음", "삭제할 QR 코드를 선택하세요.")
        return
    values = tree.item(selected, 'values')
    qr_no = values[0]
    if messagebox.askyesno("삭제 확인", "정말 삭제하시겠습니까?"):
        delete_qr(qr_no)
        refresh_dashboard()

# 간단한 입력창 함수
def simple_input(title, prompt, default_value=''):
    popup = tk.Toplevel()
    popup.title(title)
    popup.grab_set()
    tk.Label(popup, text=prompt).pack(padx=10, pady=5)
    input_var = tk.StringVar(value=default_value)
    entry = ttk.Entry(popup, textvariable=input_var)
    entry.pack(padx=10, pady=5)
    entry.focus()
    result = {'value': None}

    def submit():
        result['value'] = input_var.get()
        popup.destroy()

    ttk.Button(popup, text="확인", command=submit).pack(pady=5)
    popup.wait_window()
    return result['value']

# GUI 설정
root = tk.Tk()
root.title("QR 코드 생성 및 관리")
root.geometry("800x600")

frame_input = ttk.LabelFrame(root, text="QR 코드 정보 입력")
frame_input.pack(fill="x", padx=10, pady=5)

entry_name = ttk.Entry(frame_input, width=50)
entry_value = ttk.Entry(frame_input, width=50)
entry_path = ttk.Entry(frame_input, width=50)
btn_browse = ttk.Button(frame_input, text="폴더 선택", command=lambda: entry_path.insert(0, filedialog.askdirectory() + '/'))

entry_name.grid(row=0, column=1, padx=5, pady=5)
entry_value.grid(row=1, column=1, padx=5, pady=5)
entry_path.grid(row=2, column=1, padx=5, pady=5)
btn_browse.grid(row=2, column=2, padx=5)

tt_label = ["QR 코드 이름:", "QR 코드 값:", "저장 경로:"]
for i, txt in enumerate(tt_label):
    ttk.Label(frame_input, text=txt).grid(row=i, column=0, sticky="e", padx=5, pady=5)

btn_generate = ttk.Button(root, text="QR 코드 생성", command=generate_qr)
btn_generate.pack(pady=10)

frame_dashboard = ttk.LabelFrame(root, text="QR 코드 대시보드")
frame_dashboard.pack(fill="both", expand=True, padx=10, pady=10)

cols = ("번호", "이름", "값", "파일 경로")
tree = ttk.Treeview(frame_dashboard, columns=cols, show='headings')
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(fill="both", expand=True)

btn_edit = ttk.Button(root, text="QR 코드 이름 수정", command=on_edit)
btn_delete = ttk.Button(root, text="QR 코드 삭제", command=on_delete)
btn_edit.pack(pady=5)
btn_delete.pack(pady=5)

refresh_dashboard()
root.mainloop()

