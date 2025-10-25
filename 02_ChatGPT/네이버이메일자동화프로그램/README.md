# 네이버 이메일 자동화 (재작성)

간단한 데스크탑 GUI 도구로, DB에 저장된 이메일을 Selenium으로 네이버 메일에 전송하는 예제 프로그램입니다.

기능 요약
- 이메일 저장(CRUD)
- 일괄 전송(데이터베이스에 저장된 전송 전 항목 순차 전송)
- DB: MySQL 우선 사용, 연결 불가 시 SQLite로 자동 폴백

설치 및 실행
1. Python 3.10+ 설치
2. 의존성 설치:

```powershell
python -m pip install -r requirements.txt
```

3. Chrome과 chromedriver 설치. chromedriver가 PATH에 있어야 하거나 `browser_auto.NaverMailer(service_path=...)`로 경로를 제공하세요.

4. (선택) MySQL 사용 시 로컬에서 MySQL 서버를 실행하거나 `db_helper.DB_CONFIG`를 환경에 맞게 수정하세요.

5. 실행:

```powershell
python main.py
```

주의 및 참고
- 네이버의 로그인/메일 UI는 수시로 변경될 수 있습니다. 전송 실패가 발생하면 `browser_auto.py`의 셀렉터(아이디/클래스)를 확인하고 조정하세요.
- 이 프로그램은 교육용/자동화 예제입니다. 실제 계정/대량 전송 시 네이버의 이용 약관과 스팸 정책을 준수하세요.
# 네이버 이메일 자동화 (초기 구현)

이 저장소는 네이버 메일을 자동으로 로그인하고, DB에 저장된 이메일을 일괄 전송하는 간단한 GUI 도구의 초기 구현입니다.

주요 기능
- MySQL에 이메일 데이터 저장 (테이블이 없으면 자동 생성)
- tkinter GUI로 이메일 등록/수정/삭제
- Selenium을 사용한 네이버 로그인 및 메일 전송

설치
1. Python 3.13 환경을 준비하세요.
2. requirements.txt 설치:

```
pip install -r requirements.txt
```

3. Chrome과 chromedriver(버전 일치)를 설치하고 chromedriver가 PATH에 있거나 `browser_auto.NaverMailer` 생성 시 `driver_path`로 경로를 넘겨주세요.

MySQL 설정
- DB: `python`
- 사용자: `python` / 비밀번호: `123456`

프로그램 실행

```
python main.py
```

사용법 요약
- NAVER ID/PW 입력 후 "로그인 (브라우저 열기)" 클릭하면 브라우저가 열리고 로그인 시도합니다.
- 이메일 항목을 입력한 뒤 "메일 등록"으로 DB에 저장합니다.
- 리스트에서 선택 후 "수정" 또는 "삭제"로 항목을 관리합니다.
- "일괄 전송"을 누르면 DB의 전송되지 않은 메일들을 순차적으로 전송하고 전송 완료 시 status를 '완료'로 변경합니다.

참고 및 제약
- 네이버 로그인 및 메일 UI는 변경될 수 있으므로, 에디터나 버튼의 selector가 다르면 코드 수정이 필요합니다.
- chromedriver와 Chrome 버전이 맞아야 정상 동작합니다.
