# textMonitor

textMonitor는 python Flask 기반의 웹 애플리케이션으로, 사용자가 기사(Article)를 읽고 상호작용하는 동안 방문 시간, 메모, 피드백, 평가 등을 기록하여 분석할 수 있도록 돕는 시스템입니다. 

⸻

## 📁 프로젝트 폴더 구조

```
textMonitor/
├── app.py                      # 메인 Flask 앱 실행 파일
├── README.md                   # 프로젝트 설명 문서
├── requirements.txt            # 필요한 Python 패키지 목록
├── .gitignore                  
│
├── migrations/                 # Flask-Migrate DB 마이그레이션 폴더
│   └── versions/               # 마이그레이션 히스토리
│
├── static/                     # static resources (CSS, JS)
│   ├── article.js
│   ├── js/index.js
│   ├── preventBack.js
│   └── styles.css
│
├── templates/                  # HTML Template (Jinja2)
│   ├── article/
│   │   ├── add_article.html
│   │   ├── article.html
│   │   └── edit_article.html
│   ├── base.html
│   ├── end.html
│   ├── index.html
│   ├── login.html
│   ├── preventBack.html
│   └── register.html
│
├── tester/                     # 테스트 코드 폴더
│   └── tester.py
```

⸻


## 🧭 주요 기능
	•	회원가입 및 로그인
	•	임의의 순서로 기사 노출
	•	기사 조회 및 머무른 시간 기록
	•	기사별 메모 작성
	•	기사 평가 및 피드백 제출 
	•	개인 또는 전체 사용자 데이터 엑셀 추출
	•	관리자 전용: 기사 추가/수정/삭제 인터페이스
	•	초기화 기능 (DB 초기화 및 결과파일 생성)

⸻

## ⚙️ 설치 및 실행 방법 (Mac 기준)

1. 프로젝트 클론

```bash
git clone https://github.com/blowthehwistle/textMonitor.git
cd textMonitor
```
2. 가상환경 생성 및 활성화

```bash
python3 -m venv venv
source venv/bin/activate  # (Windows는 .\venv\Scripts\activate)
```

3. 패키지 설치

```bash
pip install -r requirements.txt
```

4. 데이터베이스 업데이트

```bash
flask db migrate
flask db upgrade
```

또는 이미 설정된 DB가 있다면 생략 가능


5. 서버 실행

```bash
python3 app.py
```

6. 브라우저에서 확인

웹 브라우저에서 다음 주소로 접속:

http://localhost:5000


⸻


## 📊 주요 라우트 요약

URL	설명
/	로그인 페이지로 리디렉션
/index	기사 피드 페이지 (무작위 노출)
/article/<id>	특정 기사 보기
/edit_article	관리자 전용 편집 페이지
/add_article	기사 추가 페이지
/record	방문 정보 저장 (AJAX)
/save-memo	메모 저장 (AJAX)
/submit-feedback	피드백 제출
/rate	기사 평가 저장
/export-to-excel	사용자 개인 데이터 엑셀 다운로드
/export-all-to-excel	관리자 전용 전체 사용자 데이터 압축 다운로드
/refresh	DB 초기화 (관리자 전용)


⸻

## 🛠 기술 스택
	•	Backend: Python, Flask
	•	Frontend: Jinja2, HTML/CSS
	•	Database: SQLite, SQLAlchemy
	•	엑셀 처리: pandas, openpyxl, zipfile

⸻

## 🔐 관리자 계정 안내


관리자 권한으로 전체 데이터를 다운로드하거나 기사를 관리하려면, 사용자명 admin 계정을 직접 DB에 생성하거나 수동으로 가입 후 권한 부여 필요

⸻

## 📝 라이선스

본 프로젝트는 MIT 라이선스를 따릅니다.