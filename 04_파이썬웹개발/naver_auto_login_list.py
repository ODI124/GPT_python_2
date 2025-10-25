import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import threading
try:
    import openpyxl
except Exception:
    openpyxl = None

class NaverAutoLogin:
    def __init__(self):
        self.driver = None
        self.setup_gui()
    
    def setup_gui(self):
        # 메인 윈도우 설정
        self.root = tk.Tk()
        self.root.title("네이버 자동 로그인")
        self.root.geometry("350x450")
        self.root.resizable(False, False)
        
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="네이버 자동 로그인", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # 아이디 입력
        ttk.Label(main_frame, text="아이디:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.id_entry = ttk.Entry(main_frame, width=30)
        self.id_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # 비밀번호 입력
        ttk.Label(main_frame, text="비밀번호:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.pw_entry = ttk.Entry(main_frame, width=30, show="*")
        self.pw_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        
        # 헤드리스 모드 체크박스
        self.headless_var = tk.BooleanVar()
        headless_check = ttk.Checkbutton(main_frame, text="백그라운드 실행 (헤드리스 모드)", 
                                       variable=self.headless_var)
        headless_check.grid(row=4, column=0, columnspan=2, pady=10)
        
        # 로그인 버튼
        login_btn = ttk.Button(main_frame, text="로그인", command=self.auto_login,
                              style="Accent.TButton")
        login_btn.grid(row=5, column=0, columnspan=2, pady=6, ipadx=20)

        # 엑셀에서 일괄 로그인 버튼
        batch_btn = ttk.Button(main_frame, text="엑셀에서 로그인", command=self.on_batch_click)
        batch_btn.grid(row=6, column=0, columnspan=2, pady=6)

        # 상태 표시
        self.status_label = ttk.Label(main_frame, text="로그인 정보를 입력하고 '로그인' 버튼을 클릭하세요.",
                                      foreground="blue")
        self.status_label.grid(row=7, column=0, columnspan=2, pady=10)

        # 닫기 버튼
        close_btn = ttk.Button(main_frame, text="종료", command=self.close_application)
        close_btn.grid(row=8, column=0, columnspan=2, pady=10)
   
   
    def auto_login(self):
        """자동 로그인 실행"""
        # 입력값 검증
        user_id = self.id_entry.get().strip()
        user_pw = self.pw_entry.get().strip()
        
        if not user_id or not user_pw:
            messagebox.showwarning("입력 오류", "아이디와 비밀번호를 모두 입력해주세요.")
            return
        
        self.status_label.config(text="로그인 중...", foreground="orange")
        self.root.update()
        
        try:
            # 페이지 로딩 대기
            wait = WebDriverWait(self.driver, 10)
            
            # 아이디 입력창 찾기 및 입력 (JavaScript 사용)
            self.status_label.config(text="아이디 입력 중...")
            self.root.update()
            
            # 아이디 입력 필드가 로드될 때까지 대기
            wait.until(EC.presence_of_element_located((By.ID, "id")))
            
            # JavaScript로 아이디 입력 (send_keys 우회)
            self.driver.execute_script(f"""
                var idField = document.getElementById('id');
                idField.value = '';
                idField.value = '{user_id}';
                idField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                idField.dispatchEvent(new Event('change', {{ bubbles: true }}));
            """)
            
            time.sleep(1)  # 잠깐 대기
            
            # 비밀번호 입력창 찾기 및 입력 (JavaScript 사용)
            self.status_label.config(text="비밀번호 입력 중...")
            self.root.update()
            
            # 비밀번호 입력 필드가 로드될 때까지 대기
            wait.until(EC.presence_of_element_located((By.ID, "pw")))
            
            # JavaScript로 비밀번호 입력 (send_keys 우회)
            self.driver.execute_script(f"""
                var pwField = document.getElementById('pw');
                pwField.value = '';
                pwField.value = '{user_pw}';
                pwField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                pwField.dispatchEvent(new Event('change', {{ bubbles: true }}));
            """)
            
            time.sleep(1)  # 잠깐 대기
            
            # 로그인 버튼 클릭
            self.status_label.config(text="로그인 버튼 클릭 중...")
            self.root.update()
            
            login_button = wait.until(EC.element_to_be_clickable((By.ID, "log.login")))
            login_button.click()
            
            # 로그인 결과 확인 (페이지 변경 대기)
            time.sleep(3)
            
            current_url = self.driver.current_url
            
            # 로그인 성공 여부 확인
            if "nid.naver.com" not in current_url or "naver.com" in current_url:
                self.status_label.config(text="로그인 성공! 브라우저에서 네이버를 이용하세요.", foreground="green")
                messagebox.showinfo("성공", "네이버 로그인이 완료되었습니다!")
            else:
                # 오류 메시지 확인
                try:
                    error_element = self.driver.find_element(By.CLASS_NAME, "error_msg")
                    error_msg = error_element.text
                    self.status_label.config(text=f"로그인 실패: {error_msg}", foreground="red")
                    messagebox.showerror("로그인 실패", f"로그인에 실패했습니다.\n{error_msg}")
                except:
                    self.status_label.config(text="로그인 실패: 아이디 또는 비밀번호를 확인하세요.", foreground="red")
                    messagebox.showerror("로그인 실패", "로그인에 실패했습니다.\n아이디 또는 비밀번호를 확인하세요.")
            
        except Exception as e:
            self.status_label.config(text="오류 발생", foreground="red")
            messagebox.showerror("오류", f"로그인 중 오류가 발생했습니다:\n{str(e)}")
        
        # 드라이버는 열어둠 (사용자가 브라우저에서 네이버 이용 가능)
    
    def close_application(self):
        """프로그램 종료"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        self.root.destroy()
    
    def run(self):
        """GUI 실행"""
        # 브라우저 실행
        # 기본적으로는 드라이버를 나중에 생성 (배치 실행시 각각 생성)
        # 단, GUI를 통한 수동 로그인 시에는 드라이버를 바로 실행
        # self.run_chrome()
        # 윈도우 닫기 이벤트 처리
        self.root.protocol("WM_DELETE_WINDOW", self.close_application)
        self.root.mainloop()
        
    def run_chrome(self):
        options = Options()
        if self.headless_var.get():
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
                
        # 사용자 에이전트 설정 (봇 탐지 방지)
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # 브라우저 실행        
        self.driver = webdriver.Chrome(options=options)
        # 네이버 로그인 페이지 접속
        self.driver.get("https://nid.naver.com/nidlogin.login")

    def create_driver(self):
        """Create a Chrome webdriver instance according to GUI options and return it (caller must quit)."""
        options = Options()
        if self.headless_var.get():
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        driver = webdriver.Chrome(options=options)
        return driver

    def load_credentials_from_excel(self, file_path):
        """Read credentials from an Excel file with columns: 번호, 아이디, 비밀번호. Return list of dicts."""
        if openpyxl is None:
            messagebox.showerror("의존성 오류", "openpyxl이 설치되어 있지 않습니다. 'pip install openpyxl'로 설치해주세요.")
            return []
        try:
            wb = openpyxl.load_workbook(file_path, data_only=True)
            ws = wb.active
            creds = []
            # assume header in first row
            rows = list(ws.iter_rows(values_only=True))
            if not rows:
                return []
            header = [str(c).strip() if c is not None else "" for c in rows[0]]
            # find indices
            try:
                idx_id = header.index('아이디')
                idx_pw = header.index('비밀번호')
            except ValueError:
                # fallback to common indices
                idx_id = 1
                idx_pw = 2
            for r in rows[1:]:
                if r is None:
                    continue
                uid = r[idx_id] if idx_id < len(r) else None
                upw = r[idx_pw] if idx_pw < len(r) else None
                if uid and upw:
                    creds.append({'id': str(uid).strip(), 'pw': str(upw).strip()})
            return creds
        except Exception as e:
            messagebox.showerror("파일 오류", f"엑셀 파일을 읽는 중 오류가 발생했습니다:\n{e}")
            return []

    def perform_login_once(self, driver, user_id, user_pw, status_callback=None, timeout=10):
        """Perform login using provided driver, return True on success, False otherwise."""
        try:
            wait = WebDriverWait(driver, timeout)
            driver.get("https://nid.naver.com/nidlogin.login")
            if status_callback:
                status_callback(f"아이디 입력 중... {user_id}")
            wait.until(EC.presence_of_element_located((By.ID, 'id')))
            driver.execute_script(f"var idField = document.getElementById('id'); idField.value = ''; idField.value = '{user_id}'; idField.dispatchEvent(new Event('input', {{ bubbles: true }})); idField.dispatchEvent(new Event('change', {{ bubbles: true }}));")
            time.sleep(0.8)
            if status_callback:
                status_callback("비밀번호 입력 중...")
            wait.until(EC.presence_of_element_located((By.ID, 'pw')))
            driver.execute_script(f"var pwField = document.getElementById('pw'); pwField.value = ''; pwField.value = '{user_pw}'; pwField.dispatchEvent(new Event('input', {{ bubbles: true }})); pwField.dispatchEvent(new Event('change', {{ bubbles: true }}));")
            time.sleep(0.8)
            if status_callback:
                status_callback("로그인 버튼 클릭 중...")
            login_button = wait.until(EC.element_to_be_clickable((By.ID, 'log.login')))
            login_button.click()
            time.sleep(3)
            current_url = driver.current_url
            # simple heuristic: if not still on Naver login domain, consider login successful
            if 'nid.naver.com' not in current_url and 'naver.com' in current_url:
                if status_callback:
                    status_callback("로그인 성공")
                return True
            # try to read possible error message
            try:
                error_element = driver.find_element(By.CLASS_NAME, 'error_msg')
                error_msg = error_element.text
                if status_callback:
                    status_callback(f"로그인 실패: {error_msg}")
            except Exception:
                if status_callback:
                    status_callback("로그인 실패: 아이디 또는 비밀번호 확인")
            return False
        except Exception as e:
            if status_callback:
                status_callback(f"오류: {e}")
            return False

    def batch_login_from_excel(self, file_path=None):
        """Read credentials and sequentially login/logout each account."""
        # resolve file path
        if file_path is None:
            default_path = os.path.join(os.path.dirname(__file__), '네이버아이디.xlsx')
            if os.path.exists(default_path):
                file_path = default_path
            else:
                file_path = filedialog.askopenfilename(title='아이디 엑셀 파일 선택', filetypes=[('Excel files', '*.xlsx;*.xls')])
                if not file_path:
                    return
        creds = self.load_credentials_from_excel(file_path)
        if not creds:
            messagebox.showinfo('정보', '로그인할 계정이 없습니다.')
            return
        total = len(creds)
        for i, c in enumerate(creds, start=1):
            uid = c['id']
            upw = c['pw']
            self.status_label.config(text=f"{i}/{total} - {uid} 로그인 시도...", foreground='orange')
            self.root.update()
            driver = None
            try:
                driver = self.create_driver()
                ok = self.perform_login_once(driver, uid, upw, status_callback=lambda s: self._update_status(s))
                if ok:
                    messagebox.showinfo('성공', f"{uid} 로그인 성공, 로그아웃합니다.")
                    # perform logout by visiting logout URL
                    try:
                        driver.get('https://nid.naver.com/nidlogin.logout?returl=https://www.naver.com')
                        time.sleep(2)
                    except Exception:
                        pass
                else:
                    messagebox.showwarning('실패', f"{uid} 로그인에 실패했습니다.")
            except Exception as e:
                messagebox.showerror('오류', f"{uid} 처리 중 오류: {e}")
            finally:
                try:
                    if driver:
                        driver.quit()
                except Exception:
                    pass
        self.status_label.config(text='배치 작업 완료', foreground='green')

    def _update_status(self, text):
        try:
            self.status_label.config(text=text)
            self.root.update()
        except Exception:
            pass

    def on_batch_click(self):
        """GUI handler: ask for excel file (optional) and start batch in background thread."""
        # prefer a chosen file, but fall back to default if user cancels
        file_path = filedialog.askopenfilename(title='아이디 엑셀 파일 선택', filetypes=[('Excel files', '*.xlsx;*.xls')])
        if not file_path:
            default_path = os.path.join(os.path.dirname(__file__), '네이버아이디.xlsx')
            if os.path.exists(default_path):
                file_path = default_path
            else:
                return
        # start batch in background to keep GUI responsive
        self.status_label.config(text='배치 작업 시작...', foreground='orange')
        t = threading.Thread(target=lambda: self.batch_login_from_excel(file_path), daemon=True)
        t.start()

if __name__ == "__main__":
    app = NaverAutoLogin()
    app.run()