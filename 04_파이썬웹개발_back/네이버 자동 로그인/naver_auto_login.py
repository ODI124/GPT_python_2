import tkinter as tk
from tkinter import ttk, messagebox
from selepipnium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

class NaverAutoLogin:
    def __init__(self):
        self.driver = None
        self.setup_gui()
    
    def setup_gui(self):
        # 메인 윈도우 설정
        self.root = tk.Tk()
        self.root.title("네이버 자동 로그인")
        self.root.geometry("400x300")
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
        
        # 브라우저 선택
        ttk.Label(main_frame, text="브라우저:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.browser_var = tk.StringVar(value="Chrome")
        browser_combo = ttk.Combobox(main_frame, textvariable=self.browser_var, 
                                   values=["Chrome", "Edge"], state="readonly", width=27)
        browser_combo.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # 헤드리스 모드 체크박스
        self.headless_var = tk.BooleanVar()
        headless_check = ttk.Checkbutton(main_frame, text="백그라운드 실행 (헤드리스 모드)", 
                                       variable=self.headless_var)
        headless_check.grid(row=4, column=0, columnspan=2, pady=10)
        
        # 로그인 버튼
        login_btn = ttk.Button(main_frame, text="로그인", command=self.auto_login, 
                             style="Accent.TButton")
        login_btn.grid(row=5, column=0, columnspan=2, pady=20, ipadx=20)
        
        # 상태 표시
        self.status_label = ttk.Label(main_frame, text="로그인 정보를 입력하고 '로그인' 버튼을 클릭하세요.", 
                                    foreground="blue")
        self.status_label.grid(row=6, column=0, columnspan=2, pady=10)
        
        # 닫기 버튼
        close_btn = ttk.Button(main_frame, text="종료", command=self.close_application)
        close_btn.grid(row=7, column=0, columnspan=2, pady=10)
    
    def setup_driver(self):
        """브라우저 드라이버 설정"""
        try:
            if self.browser_var.get() == "Chrome":
                options = Options()
                if self.headless_var.get():
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                
                # 사용자 에이전트 설정 (봇 탐지 방지)
                options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                
                self.driver = webdriver.Chrome(options=options)
            
            elif self.browser_var.get() == "Edge":
                from selenium.webdriver.edge.options import Options as EdgeOptions
                from selenium.webdriver.edge.service import Service as EdgeService
                
                options = EdgeOptions()
                if self.headless_var.get():
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                
                self.driver = webdriver.Edge(options=options)
            
            return True
            
        except Exception as e:
            messagebox.showerror("오류", f"브라우저 드라이버 설정 실패:\n{str(e)}\n\n브라우저 드라이버가 설치되어 있는지 확인하세요.")
            return False
    
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
            # 드라이버 설정
            if not self.setup_driver():
                return
            
            # 네이버 로그인 페이지 접속
            self.status_label.config(text="네이버 로그인 페이지에 접속 중...")
            self.root.update()
            
            self.driver.get("https://nid.naver.com/nidlogin.login")
            
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
        # 윈도우 닫기 이벤트 처리
        self.root.protocol("WM_DELETE_WINDOW", self.close_application)
        self.root.mainloop()

if __name__ == "__main__":
    app = NaverAutoLogin()
    app.run()