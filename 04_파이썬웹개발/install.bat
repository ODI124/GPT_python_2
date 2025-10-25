@echo off
echo =====================================
echo  네이버 자동 로그인 프로그램 설치
echo =====================================
echo.
echo 필요한 라이브러리를 설치합니다...
echo.

cd /d "%~dp0"

echo [1/3] selenium 설치 중...
pip install selenium

echo.
echo [2/3] webdriver-manager 설치 중...
pip install webdriver-manager

echo.
echo [3/3] pyperclip 설치 중...
pip install pyperclip

echo.
echo =====================================
echo  설치가 완료되었습니다!
echo =====================================
echo.
echo 이제 run_naver_login.bat 파일을 실행하여
echo 네이버 자동 로그인 프로그램을 사용할 수 있습니다.
echo.
pause