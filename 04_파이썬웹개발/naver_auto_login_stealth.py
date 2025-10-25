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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json
import os
import pyperclip
import random

class NaverAutoLoginStealth:
    def __init__(self):
        self.driver = None
        self.config_file = "login_config.json"
        self.setup_gui()
        self.load_config()
    
    def setup_gui(self):
        # 메인 윈도우 설정
        self.root = tk.Tk()
        self.root.title("네이버 자동 로그인 (스텔스 모드)")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        # 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')
        
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="네이버 자동 로그인 (스텔스)", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # 부제목
        subtitle_label = ttk.Label(main_frame, text="고급 우회 기술 적용", font=("Arial", 10), foreground="gray")
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        
        # 구분선
        separator1 = ttk.Separator(main_frame, orient='horizontal')
        separator1.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 로그인 정보 프레임
        login_frame = ttk.LabelFrame(main_frame, text="로그인 정보", padding="10")
        login_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
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
        
        # 우회 방법 선택 프레임
        method_frame = ttk.LabelFrame(main_frame, text="입력 방법 선택", padding="10")
        method_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.input_method = tk.StringVar(value="javascript")
        ttk.Radiobutton(method_frame, text="JavaScript 직접 입력", variable=self.input_method, value="javascript").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(method_frame, text="클립보드 + Ctrl+V", variable=self.input_method, value="clipboard").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(method_frame, text="DOM 조작", variable=self.input_method, value="dom").grid(row=2, column=0, sticky=tk.W)
        
        # 브라우저 설정 프레임
        browser_frame = ttk.LabelFrame(main_frame, text="브라우저 설정", padding="10")
        browser_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 브라우저 선택
        ttk.Label(browser_frame, text="브라우저:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.browser_var = tk.StringVar(value="Chrome")
        browser_combo = ttk.Combobox(browser_frame, textvariable=self.browser_var, 
                                   values=["Chrome", "Edge"], state="readonly", width=22)
        browser_combo.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # 스텔스 모드 체크박스
        self.stealth_var = tk.BooleanVar(value=True)
        stealth_check = ttk.Checkbutton(browser_frame, text="스텔스 모드 (봇 탐지 방지)", 
                                       variable=self.stealth_var)
        stealth_check.grid(row=1, column=0, columnspan=2, pady=5)
        
        # 헤드리스 모드 체크박스
        self.headless_var = tk.BooleanVar()
        headless_check = ttk.Checkbutton(browser_frame, text="백그라운드 실행", 
                                       variable=self.headless_var)
        headless_check.grid(row=2, column=0, columnspan=2, pady=5)
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=15)
        
        # 로그인 버튼
        login_btn = ttk.Button(button_frame, text="스텔스 로그인", command=self.auto_login, 
                             style="Accent.TButton")
        login_btn.pack(side=tk.LEFT, padx=(0, 10), ipadx=15)
        
        # 브라우저 닫기 버튼
        close_browser_btn = ttk.Button(button_frame, text="브라우저 닫기", command=self.close_browser)
        close_browser_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 종료 버튼
        close_btn = ttk.Button(button_frame, text="프로그램 종료", command=self.close_application)
        close_btn.pack(side=tk.LEFT)
        
        # 상태 표시
        self.status_label = ttk.Label(main_frame, text="로그인 정보를 입력하고 '스텔스 로그인' 버튼을 클릭하세요.", 
                                    foreground="blue", wraplength=450)
        self.status_label.grid(row=7, column=0, columnspan=2, pady=15)
        
        # 진행률 바
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
    
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
                    self.stealth_var.set(config.get('stealth', True))
                    self.input_method.set(config.get('input_method', 'javascript'))
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
                'stealth': self.stealth_var.get(),
                'input_method': self.input_method.get()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"설정 파일 저장 오류: {e}")
    
    def setup_driver(self):
        """브라우저 드라이버 설정 (스텔스 모드)"""
        try:
            if self.browser_var.get() == "Chrome":
                options = ChromeOptions()
                
                if self.headless_var.get():
                    options.add_argument("--headless")
                
                if self.stealth_var.get():
                    # 스텔스 모드 설정
                    options.add_argument("--disable-blink-features=AutomationControlled")
                    options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    options.add_experimental_option('useAutomationExtension', False)
                    options.add_argument("--disable-dev-shm-usage")
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--disable-extensions")
                    options.add_argument("--disable-plugins")
                    options.add_argument("--disable-images")
                    
                    # 랜덤 사용자 에이전트
                    user_agents = [
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
                    ]
                    options.add_argument(f"--user-agent={random.choice(user_agents)}")
                
                options.add_argument("--window-size=1920,1080")
                
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            
            elif self.browser_var.get() == "Edge":
                options = EdgeOptions()
                
                if self.headless_var.get():
                    options.add_argument("--headless")
                
                if self.stealth_var.get():
                    options.add_argument("--disable-blink-features=AutomationControlled")
                    options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    options.add_experimental_option('useAutomationExtension', False)
                
                options.add_argument("--window-size=1920,1080")
                
                service = EdgeService(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=service, options=options)
            
            # 스텔스 스크립트 실행
            if self.stealth_var.get():
                self.driver.execute_script("""
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                    Object.defineProperty(navigator, 'languages', {get: () => ['ko-KR', 'ko']});
                    window.chrome = {runtime: {}};
                """)
            
            return True
            
        except Exception as e:
            messagebox.showerror("오류", f"브라우저 드라이버 설정 실패:\n{str(e)}")
            return False
    
    def input_with_javascript(self, element_id, value):
        """JavaScript를 사용한 입력"""
        escaped_value = value.replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n')
        
        script = f"""
        var element = document.getElementById('{element_id}');
        if (element) {{
            element.value = '';
            element.value = '{escaped_value}';
            element.focus();
            
            // 다양한 이벤트 발생
            ['input', 'change', 'keydown', 'keyup', 'blur'].forEach(function(eventType) {{
                var event = new Event(eventType, {{ bubbles: true }});
                element.dispatchEvent(event);
            }});
            
            return true;
        }}
        return false;
        """
        
        return self.driver.execute_script(script)
    
    def input_with_clipboard(self, element_id, value):
        """클립보드를 사용한 입력"""
        try:
            # 클립보드에 값 복사
            pyperclip.copy(value)
            time.sleep(0.5)
            
            # 요소 클릭하여 포커스
            element = self.driver.find_element(By.ID, element_id)
            element.click()
            time.sleep(0.5)
            
            # 기존 값 삭제
            element.send_keys(Keys.CONTROL + "a")
            time.sleep(0.3)
            
            # 클립보드 내용 붙여넣기
            element.send_keys(Keys.CONTROL + "v")
            time.sleep(0.5)
            
            return True
        except Exception as e:
            print(f"클립보드 입력 오류: {e}")
            return False
    
    def input_with_dom(self, element_id, value):
        """DOM 조작을 통한 입력"""
        escaped_value = value.replace("'", "\\'").replace('"', '\\"')
        
        script = f"""
        var element = document.getElementById('{element_id}');
        if (element) {{
            // 기존 값 제거
            element.value = '';
            
            // React/Vue 등을 위한 setter 사용
            var descriptor = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value');
            if (descriptor && descriptor.set) {{
                descriptor.set.call(element, '{escaped_value}');
            }} else {{
                element.value = '{escaped_value}';
            }}
            
            // 다양한 이벤트 시뮬레이션
            element.focus();
            
            var inputEvent = new InputEvent('input', {{
                bubbles: true,
                cancelable: true,
                inputType: 'insertText',
                data: '{escaped_value}'
            }});
            element.dispatchEvent(inputEvent);
            
            var changeEvent = new Event('change', {{ bubbles: true }});
            element.dispatchEvent(changeEvent);
            
            return true;
        }}
        return false;
        """
        
        return self.driver.execute_script(script)
    
    def auto_login(self):
        """자동 로그인 실행 (스텔스 모드)"""
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
        
        self.status_label.config(text="스텔스 모드로 로그인 준비 중...", foreground="orange")
        self.root.update()
        
        try:
            # 드라이버 설정
            self.status_label.config(text="스텔스 브라우저 설정 중...")
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
            
            # 페이지가 완전히 로드될 때까지 대기
            wait.until(EC.presence_of_element_located((By.ID, "id")))
            wait.until(EC.presence_of_element_located((By.ID, "pw")))
            
            # 랜덤 대기 (자연스러운 행동 시뮬레이션)
            time.sleep(random.uniform(1.0, 2.0))
            
            # 아이디 입력
            self.status_label.config(text=f"아이디 입력 중... ({self.input_method.get()} 방식)")
            self.root.update()
            
            success = False
            if self.input_method.get() == "javascript":
                success = self.input_with_javascript("id", user_id)
            elif self.input_method.get() == "clipboard":
                success = self.input_with_clipboard("id", user_id)
            elif self.input_method.get() == "dom":
                success = self.input_with_dom("id", user_id)
            
            if not success:
                raise Exception("아이디 입력에 실패했습니다.")
            
            time.sleep(random.uniform(0.5, 1.0))
            
            # 비밀번호 입력
            self.status_label.config(text=f"비밀번호 입력 중... ({self.input_method.get()} 방식)")
            self.root.update()
            
            success = False
            if self.input_method.get() == "javascript":
                success = self.input_with_javascript("pw", user_pw)
            elif self.input_method.get() == "clipboard":
                success = self.input_with_clipboard("pw", user_pw)
            elif self.input_method.get() == "dom":
                success = self.input_with_dom("pw", user_pw)
            
            if not success:
                raise Exception("비밀번호 입력에 실패했습니다.")
            
            time.sleep(random.uniform(0.5, 1.0))
            
            # 로그인 버튼 클릭
            self.status_label.config(text="로그인 버튼 클릭...")
            self.root.update()
            
            login_button = wait.until(EC.element_to_be_clickable((By.ID, "log.login")))
            
            # JavaScript로 클릭 (더 자연스러운 클릭)
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
                self.status_label.config(text="✅ 스텔스 로그인 성공! 네이버 메인 페이지로 이동되었습니다.", foreground="green")
                messagebox.showinfo("성공", "네이버 스텔스 로그인이 완료되었습니다!")
                    
            else:
                # 오류 메시지 확인
                try:
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
                    self.status_label.config(text=f"❌ 로그인 실패: {error_msg}", foreground="red")
                    messagebox.showerror("로그인 실패", f"로그인에 실패했습니다.\n\n{error_msg}")
                    
                except Exception as e:
                    self.progress.stop()
                    self.status_label.config(text="❌ 로그인 실패: 아이디 또는 비밀번호를 확인하세요.", foreground="red")
                    messagebox.showerror("로그인 실패", "로그인에 실패했습니다.\n아이디 또는 비밀번호를 확인하세요.")
            
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="❌ 오류 발생", foreground="red")
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
    app = NaverAutoLoginStealth()
    app.run()