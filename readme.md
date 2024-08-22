# textMonitor

### textmonitorvenv
가상환경
실행하기 전에 가상환경으로 세팅해놓은 다음 실행해야 함
source textmonitorvenv/bin/activate

### tester
웹사이트의 기능을 측정하는 테스트 스크립트


## version

### 240702 v1.1
각 user에 대한 excel 추출
visit 테이블에 author_info_clicked 추가(테스트는 안해봄)
tester 코드 추가

### 240711 v1.2
각 페이지별 오류 수정
메모 저장 버튼 및 목록으로 돌아가기 버튼 수정

### 240721 v1.3
한 article에서 다른 article로 넘어가는 화면 수정 (랜덤 6개)

### 240822 v1.4
- index에서 랜덤 6개 수정(user별로 고유한 article 가지고, 기사 설정에서 display_on_index에 체크해야함)
- UI/UX 수정(버튼 스타일, 별점창 등)
- 엑셀 형식 수정
- 엑셀에 display_on_index도 반영되게 추가
- article->article 이동시 feedback창 뜨도록 수정

### Todo
- testcode에 별점 기능 추가
- testcode에서 article->article 했을 때 잘 나오는지
- article->article시 undefined로 이동하는 오류
