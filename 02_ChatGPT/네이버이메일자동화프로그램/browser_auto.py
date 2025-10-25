"""Selenium-based Naver mail helper.

Notes:
- Requires chromedriver in PATH or provide driver_path to NaverMailer(service_path=...)
- Uses explicit waits and tries to handle iframe-based editors where possible.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NaverMailer:
    def __init__(self, service_path=None, headless=False, wait=20):
        opts = Options()
        if headless:
            # Selenium 4.8+ supports --headless=new; fall back to --headless if unsupported
            try:
                opts.add_argument('--headless=new')
            except Exception:
                opts.add_argument('--headless')
            opts.add_argument('--disable-gpu')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        # Create driver
        try:
            if service_path:
                service = Service(service_path)
                self.driver = webdriver.Chrome(service=service, options=opts)
            else:
                self.driver = webdriver.Chrome(options=opts)
        except WebDriverException as e:
            raise RuntimeError(f'크롬 드라이버 실행 실패: {e}')
        self.wait = WebDriverWait(self.driver, wait)

    def close(self):
        try:
            self.driver.quit()
        except Exception:
            pass

    def login(self, nid, npw):
        """Attempt to login to Naver. Returns True on success, False otherwise."""
        self.driver.get('https://nid.naver.com/nidlogin.login?mode=form')
        try:
            id_el = self.wait.until(EC.presence_of_element_located((By.ID, 'id')))
            pw_el = self.wait.until(EC.presence_of_element_located((By.ID, 'pw')))
            id_el.clear(); id_el.send_keys(nid)
            pw_el.clear(); pw_el.send_keys(npw)
            # click login button
            try:
                btn = self.driver.find_element(By.ID, 'log.login')
                btn.click()
            except Exception:
                # fallback: submit form
                pw_el.submit()
            # wait until URL changes away from login form, or profile appears
            self.wait.until(lambda d: 'nid' not in d.current_url or 'login' not in d.current_url)
            time.sleep(1)
            return True
        except Exception:
            return False

    def _find_editor(self):
        # Try direct editor
        try:
            return self.driver.find_element(By.CLASS_NAME, 'workseditor-content')
        except Exception:
            pass
        # try iframes
        iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
        for f in iframes:
            try:
                self.driver.switch_to.frame(f)
                try:
                    el = self.driver.find_element(By.CLASS_NAME, 'workseditor-content')
                    return el
                except Exception:
                    self.driver.switch_to.default_content()
            except Exception:
                continue
        self.driver.switch_to.default_content()
        return None

    def send_email(self, recipient, subject, content, timeout=30):
        """Open new mail compose and send an email. Returns True if send completed successfully."""
        self.driver.get('https://mail.naver.com/v2/new')
        try:
            rec = self.wait.until(EC.presence_of_element_located((By.ID, 'recipient_input_element')))
            subj = self.wait.until(EC.presence_of_element_located((By.ID, 'subject_title')))

            rec.clear(); rec.send_keys(recipient)
            subj.clear(); subj.send_keys(subject)

            editor = self._find_editor()
            if editor is not None:
                try:
                    editor.click()
                    editor.clear()
                    editor.send_keys(content)
                except Exception:
                    # as last resort set innerText via JS
                    self.driver.execute_script("arguments[0].innerText = arguments[1]", editor, content)
            else:
                # try a JS fallback
                try:
                    self.driver.execute_script("document.querySelector('.workseditor-content').innerText = arguments[0]", content)
                except Exception:
                    pass

            send_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'button_write_task')))
            send_btn.click()

            # wait until done page or success indicator appears
            WebDriverWait(self.driver, timeout).until(EC.url_contains('/v2/new/done'))
            return True
        except TimeoutException:
            return False
        except Exception:
            return False
