"""네이버 이메일 자동화 GUI

간단한 tkinter 앱으로 이메일을 DB에 저장하고 Selenium으로 일괄 전송합니다.
"""

import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText

from db_helper import init_db, add_email, get_all_emails, delete_email, update_email, get_pending_emails, update_status
from browser_auto import NaverMailer


class App:
    def __init__(self, root):
        self.root = root
        root.title('네이버 이메일 자동화')

        # 로그인 frame
        f1 = tk.Frame(root)
        f1.pack(fill='x', padx=8, pady=6)
        tk.Label(f1, text='NAVER ID').grid(row=0, column=0)
        self.nid = tk.Entry(f1)
        self.nid.grid(row=0, column=1)
        tk.Label(f1, text='NAVER PW').grid(row=0, column=2)
        self.npw = tk.Entry(f1, show='*')
        self.npw.grid(row=0, column=3)
        self.login_btn = tk.Button(f1, text='로그인 (브라우저 열기)', command=self._login)
        self.login_btn.grid(row=0, column=4, padx=6)

        # compose frame
        f2 = tk.Frame(root)
        f2.pack(fill='x', padx=8, pady=6)
        tk.Label(f2, text='받는사람').grid(row=0, column=0)
        self.recipient = tk.Entry(f2, width=40)
        self.recipient.grid(row=0, column=1, columnspan=3)
        tk.Label(f2, text='제목').grid(row=1, column=0)
        self.subject = tk.Entry(f2, width=60)
        self.subject.grid(row=1, column=1, columnspan=4, sticky='we')
        tk.Label(f2, text='내용').grid(row=2, column=0)
        self.content = ScrolledText(f2, height=6, width=60)
        self.content.grid(row=2, column=1, columnspan=4)

        btn_frame = tk.Frame(root)
        btn_frame.pack(fill='x', padx=8, pady=6)
        tk.Button(btn_frame, text='메일 등록', command=self._add_email).pack(side='left')
        tk.Button(btn_frame, text='삭제', command=self._delete_selected).pack(side='left', padx=6)
        tk.Button(btn_frame, text='수정', command=self._edit_selected).pack(side='left')
        tk.Button(btn_frame, text='일괄 전송', command=self._bulk_send).pack(side='right')

        # list
        self.listbox = tk.Listbox(root, width=100, height=10)
        self.listbox.pack(padx=8, pady=6)
        self.listbox.bind('<Double-1>', lambda e: self._load_selected())

        # status
        self.status_var = tk.StringVar(value='준비')
        tk.Label(root, textvariable=self.status_var).pack(anchor='w', padx=8)

        self.mailer = None

        init_db()
        self._refresh_list()

    def _set_status(self, text):
        self.status_var.set(text)

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for row in get_all_emails():
            display = f"{row['id']} | {row['recipient']} | {row.get('subject','')} | {row.get('status','')}"
            self.listbox.insert(tk.END, display)

    def _add_email(self):
        r = self.recipient.get().strip()
        s = self.subject.get().strip()
        c = self.content.get('1.0', 'end').strip()
        if not r:
            messagebox.showwarning('오류', '받는사람을 입력하세요')
            return
        add_email(r, s, c)
        self.recipient.delete(0, tk.END)
        self.subject.delete(0, tk.END)
        self.content.delete('1.0', 'end')
        self._refresh_list()

    def _get_selected_id(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        text = self.listbox.get(sel[0])
        return int(text.split('|', 1)[0].strip())

    def _delete_selected(self):
        eid = self._get_selected_id()
        if eid is None:
            messagebox.showinfo('정보', '항목을 선택하세요')
            return
        delete_email(eid)
        self._refresh_list()

    def _edit_selected(self):
        eid = self._get_selected_id()
        if eid is None:
            messagebox.showinfo('정보', '항목을 선택하세요')
            return
        rows = get_all_emails()
        row = next((r for r in rows if r['id'] == eid), None)
        if not row:
            return
        recipient = simpledialog.askstring('수정', '받는사람', initialvalue=row['recipient'])
        subject = simpledialog.askstring('수정', '제목', initialvalue=row.get('subject',''))
        content = simpledialog.askstring('수정', '내용', initialvalue=row.get('content',''))
        if recipient is not None:
            update_email(eid, recipient, subject or '', content or '')
            self._refresh_list()

    def _load_selected(self):
        eid = self._get_selected_id()
        if eid is None:
            return
        rows = get_all_emails()
        row = next((r for r in rows if r['id'] == eid), None)
        if not row:
            return
        self.recipient.delete(0, tk.END); self.recipient.insert(0, row['recipient'])
        self.subject.delete(0, tk.END); self.subject.insert(0, row.get('subject',''))
        self.content.delete('1.0', 'end'); self.content.insert('1.0', row.get('content',''))

    def _login(self):
        nid = self.nid.get().strip()
        npw = self.npw.get().strip()
        if not nid or not npw:
            messagebox.showwarning('오류', '아이디와 비밀번호를 입력하세요')
            return
        self._set_status('브라우저 열고 로그인 중...')

        def job():
            try:
                self.mailer = NaverMailer()
                ok = self.mailer.login(nid, npw)
                if ok:
                    self.root.after(0, lambda: self._set_status('로그인 성공'))
                    self.root.after(0, lambda: messagebox.showinfo('로그인', '로그인 성공'))
                else:
                    self.root.after(0, lambda: self._set_status('로그인 실패'))
                    self.root.after(0, lambda: messagebox.showerror('로그인', '로그인 실패'))
            except Exception as e:
                self.root.after(0, lambda: self._set_status('오류'))
                self.root.after(0, lambda: messagebox.showerror('오류', str(e)))

        threading.Thread(target=job, daemon=True).start()

    def _bulk_send(self):
        if self.mailer is None:
            messagebox.showwarning('경고', '먼저 로그인 해주세요 (브라우저 열기)')
            return
        pending = get_pending_emails()
        if not pending:
            messagebox.showinfo('정보', '전송할 메일이 없습니다')
            return

        self._set_status('일괄 전송 시작')

        def job():
            sent_count = 0
            for row in pending:
                rid = row['id']
                recip = row.get('recipient') or ''
                subj = row.get('subject') or ''
                cont = row.get('content') or ''
                self.root.after(0, lambda r=rid, t=recip: self._set_status(f"전송 중: {r} -> {t}"))
                ok = self.mailer.send_email(recip, subj, cont)
                if ok:
                    update_status(rid, '완료')
                    sent_count += 1
                else:
                    update_status(rid, '전송실패')
                self.root.after(0, self._refresh_list)
            self.root.after(0, lambda: self._set_status('일괄 전송 완료'))
            self.root.after(0, lambda: messagebox.showinfo('완료', f'일괄 전송이 완료되었습니다. 성공: {sent_count}/{len(pending)}'))

        threading.Thread(target=job, daemon=True).start()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
