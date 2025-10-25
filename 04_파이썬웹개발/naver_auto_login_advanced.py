import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import json
import os

class NaverAutoLoginAdvanced:
    def __init__(self):
        self.driver = None
        self.config_file = "login_config.json"
        self.setup_gui()
        self.load_config()
    
    def setup_gui(self):
        # 메인 윈도우 설정
        self.root = tk.Tk()
        self.root.title("네이버 자동 로그인 (고급)")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        
        # 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')
        
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="네이버 자동 로그인", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 구분선
        separator1 = ttk.Separator(main_frame, orient='horizontal')
        separator1.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 로그인 정보 프레임
        login_frame = ttk.LabelFrame(main_frame, text="로그인 정보", padding="10")
        login_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 아이디 입력
        ttk.Label(login_frame, text="아이디:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.id_entry = ttk.Entry(login_frame, width=25)
        self.id_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # 비밀번호 입력
        ttk.Label(login_frame, text="비밀번호:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pw_entry = ttk.Entry(login_frame, width=25, show="*")
        self.pw_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # 아이디 저장 체크박스
        self.save_id_var = tk.BooleanVar()
        save_id_check = ttk.Checkbutton(login_frame, text="아이디 저장", variable=self.save_id_var)
        save_id_check.grid(row=2, column=0, columnspan=2, pady=5)
        
        # 브라우저 설정 프레임
        browser_frame = ttk.LabelFrame(main_frame, text="브라우저 설정", padding="10")
        browser_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 브라우저 선택
        ttk.Label(browser_frame, text="브라우저:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.browser_var = tk.StringVar(value="Chrome")
        browser_combo = ttk.Combobox(browser_frame, textvariable=self.browser_var, 
                                   values=["Chrome", "Edge"], state="readonly", width=22)
        browser_combo.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # 헤드리스 모드 체크박스
        self.headless_var = tk.BooleanVar()
        headless_check = ttk.Checkbutton(browser_frame, text="백그라운드 실행 (헤드리스 모드)", 
                                       variable=self.headless_var)
        headless_check.grid(row=1, column=0, columnspan=2, pady=5)
        
        # 자동 닫기 체크박스
        self.auto_close_var = tk.BooleanVar()
        auto_close_check = ttk.Checkbutton(browser_frame, text="로그인 후 브라우저 자동 닫기", 
                                         variable=self.auto_close_var)
        auto_close_check.grid(row=2, column=0, columnspan=2, pady=5)
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        # 로그인 버튼
        login_btn = ttk.Button(button_frame, text="로그인 시작", command=self.auto_login, 
                             style="Accent.TButton")
        login_btn.pack(side=tk.LEFT, padx=(0, 10), ipadx=15)
        
        # 브라우저 닫기 버튼
        close_browser_btn = ttk.Button(button_frame, text="브라우저 닫기", command=self.close_browser)
        close_browser_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 종료 버튼
        close_btn = ttk.Button(button_frame, text="프로그램 종료", command=self.close_application)
        close_btn.pack(side=tk.LEFT)
        
        # 상태 표시
        self.status_label = ttk.Label(main_frame, text="로그인 정보를 입력하고 '로그인 시작' 버튼을 클릭하세요.", 
                                    foreground="blue", wraplength=400)
        self.status_label.grid(row=5, column=0, columnspan=2, pady=15)
        
        # 진행률 바
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
    
    def load_config(self):
        """저장된 설정 불러오기"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if config.get('save_id') and config.get('user_id'):
                        self.id_entry.insert(0, config['user_id'])
                        self.save_id_var.set(True)
                    
                    self.browser_var.set(config.get('browser', 'Chrome'))
                    self.headless_var.set(config.get('headless', False))
                    self.auto_close_var.set(config.get('auto_close', False))
        except Exception as e:
            print(f"설정 파일 로드 오류: {e}")
    
    def save_config(self):
        """설정 저장"""
        try:
            config = {
                'save_id': self.save_id_var.get(),
                'user_id': self.id_entry.get() if self.save_id_var.get() else '',
                'browser': self.browser_var.get(),
                'headless': self.headless_var.get(),
                'auto_close': self.auto_close_var.get()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"설정 파일 저장 오류: {e}")
    
    def setup_driver(self):
        """브라우저 드라이버 설정 (webdriver-manager 사용)"""
        try:
            if self.browser_var.get() == "Chrome":
                options = ChromeOptions()
                if self.headless_var.get():
                    options.add_argument("--headless")
                
                # 추가 옵션들
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                
                # 사용자 에이전트 설정
                options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                
                # webdriver-manager로 자동 드라이버 관리
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            
            elif self.browser_var.get() == "Edge":
                options = EdgeOptions()
                if self.headless_var.get():
                    options.add_argument("--headless")
                
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                
                # webdriver-manager로 자동 드라이버 관리
                service = EdgeService(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=service, options=options)
            
            # 자동화 탐지 방지
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return True
            
        except Exception as e:
            messagebox.showerror("오류", f"브라우저 드라이버 설정 실패:\n{str(e)}")
            return False
    
    def auto_login(self):
        """자동 로그인 실행"""
        # 입력값 검증
        user_id = self.id_entry.get().strip()
        user_pw = self.pw_entry.get().strip()
        
        if not user_id or not user_pw:
            messagebox.showwarning("입력 오류", "아이디와 비밀번호를 모두 입력해주세요.")
            return
        
        # 설정 저장
        self.save_config()
        
        # 진행률 바 시작
        self.progress.start(10)
        
        self.status_label.config(text="로그인 준비 중...", foreground="orange")
        self.root.update()
        
        try:
            # 드라이버 설정
            self.status_label.config(text="브라우저 드라이버 설정 중...")
            self.root.update()
            
            if not self.setup_driver():
                self.progress.stop()
                return
            
            # 네이버 로그인 페이지 접속
            self.status_label.config(text="네이버 로그인 페이지 접속 중...")
            self.root.update()
            
            self.driver.get("https://nid.naver.com/nidlogin.login")
            
            # 페이지 로딩 대기
            wait = WebDriverWait(self.driver, 15)
            
            # 아이디 입력창 찾기 및 입력 (JavaScript 사용)
            self.status_label.config(text="아이디 입력 중...")
            self.root.update()
            
            # 아이디 입력 필드가 로드될 때까지 대기
            wait.until(EC.presence_of_element_located((By.ID, "id")))
            
            # SQL 인젝션 방지를 위한 문자열 이스케이프
            escaped_id = user_id.replace("'", "\\'").replace('"', '\\"')
            
            # JavaScript로 아이디 입력 (send_keys 우회)
            self.driver.execute_script(f"""
                var idField = document.getElementById('id');
                if (idField) {{
                    idField.value = '';
                    idField.value = '{escaped_id}';
                    idField.focus();
                    idField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    idField.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    idField.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                }}
            """)
            
            time.sleep(1)
            
            # 비밀번호 입력창 찾기 및 입력 (JavaScript 사용)
            self.status_label.config(text="비밀번호 입력 중...")
            self.root.update()
            
            # 비밀번호 입력 필드가 로드될 때까지 대기
            wait.until(EC.presence_of_element_located((By.ID, "pw")))
            
            # 비밀번호 문자열 이스케이프
            escaped_pw = user_pw.replace("'", "\\'").replace('"', '\\"')
            
            # JavaScript로 비밀번호 입력 (send_keys 우회)
            self.driver.execute_script(f"""
                var pwField = document.getElementById('pw');
                if (pwField) {{
                    pwField.value = '';
                    pwField.value = '{escaped_pw}';
                    pwField.focus();
                    pwField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    pwField.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    pwField.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                }}
            """)
            
            time.sleep(1)
            
            # 로그인 버튼 클릭
            self.status_label.config(text="로그인 버튼 클릭...")
            self.root.update()
            
            login_button = wait.until(EC.element_to_be_clickable((By.ID, "log.login")))
            self.driver.execute_script("arguments[0].click();", login_button)
            
            # 로그인 결과 확인
            self.status_label.config(text="로그인 결과 확인 중...")
            self.root.update()
            
            time.sleep(3)
            
            # 현재 URL 확인
            current_url = self.driver.current_url
            
            # 로그인 성공 여부 확인
            if "naver.com" in current_url and "nidlogin" not in current_url:
                self.progress.stop()
                self.status_label.config(text="로그인 성공! 네이버 메인 페이지로 이동되었습니다.", foreground="green")
                messagebox.showinfo("성공", "네이버 로그인이 완료되었습니다!")
                
                # 자동 닫기 설정이 되어있으면 잠시 후 브라우저 닫기
                if self.auto_close_var.get():
                    self.root.after(3000, self.close_browser)  # 3초 후 자동 닫기
                    
            else:
                # 오류 메시지 확인
                try:
                    # 다양한 오류 메시지 선택자 확인
                    error_selectors = [
                        ".error_msg",
                        "#err_common",
                        ".alert_msg",
                        "[role='alert']"
                    ]
                    
                    error_msg = "알 수 없는 오류가 발생했습니다."
                    for selector in error_selectors:
                        try:
                            error_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                            if error_element.text.strip():
                                error_msg = error_element.text.strip()
                                break
                        except:
                            continue
                    
                    self.progress.stop()
                    self.status_label.config(text=f"로그인 실패: {error_msg}", foreground="red")
                    messagebox.showerror("로그인 실패", f"로그인에 실패했습니다.\n\n{error_msg}")
                    
                except Exception as e:
                    self.progress.stop()
                    self.status_label.config(text="로그인 실패: 아이디 또는 비밀번호를 확인하세요.", foreground="red")
                    messagebox.showerror("로그인 실패", "로그인에 실패했습니다.\n아이디 또는 비밀번호를 확인하세요.")
            
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="오류 발생", foreground="red")
            messagebox.showerror("오류", f"로그인 중 오류가 발생했습니다:\n{str(e)}")
    
    def close_browser(self):
        """브라우저만 닫기"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                self.status_label.config(text="브라우저가 닫혔습니다.", foreground="blue")
            except Exception as e:
                print(f"브라우저 닫기 오류: {e}")
    
    def close_application(self):
        """프로그램 종료"""
        self.close_browser()
        self.root.destroy()
    
    def run(self):
        """GUI 실행"""
        # 윈도우 닫기 이벤트 처리
        self.root.protocol("WM_DELETE_WINDOW", self.close_application)
        
        # 엔터 키 이벤트 바인딩
        self.root.bind('<Return>', lambda event: self.auto_login())
        
        self.root.mainloop()

if __name__ == "__main__":
    app = NaverAutoLoginAdvanced()
    app.run()