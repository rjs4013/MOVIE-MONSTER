# MOVIE MONSTER

MOVIE MONSTER는 영화 검색, 리뷰 작성, 게임을 통한 포인트 적립, 그리고 사용자 랭킹 시스템을 제공하는 영화 서비스 웹 애플리케이션입니다. 영화 애호가들을 위한 종합 플랫폼으로, 영화 정보를 탐색하고, 리뷰를 작성하며, 게임으로 즐거움을 느낄 수 있도록 설계되었습니다.


### 📖 목차
1. 프로젝트 소개
2. 주요 기능
3. 제작 과정
4. 기술 스택
5. 사용 방법


### 🎥 프로젝트 소개

MOVIE MONSTER는 사용자들이 영화 정보를 탐색하고, 리뷰를 공유하며, 랭킹 시스템을 통해 경쟁할 수 있는 영화 웹 플랫폼입니다. 다양한 영화 관련 기능과 현대적인 UI/UX를 갖추어 사용자 경험을 극대화했습니다.


### 🌟 주요 기능
#### 🔗 HOME 페이지
- 로그인 후 사용자 정보를 표시 (프로필 사진, 이름).
- 금주 사용자 랭킹:
    - 포인트 기반 상위 유저의 랭킹 노출.
- 추천 영화:
    - 1등 유저의 추천 영화 리스트를 한눈에 확인 가능.
- 금주 베스트 리뷰:
    - 포스터, 유저명, 별점, 영화 제목, 리뷰 내용, 좋아요 수, 작성일 표시.
    - 리뷰 클릭 시 상세 페이지로 이동.
- 커뮤니티-리뷰 작성으로의 간편 이동 버튼 제공.

#### 🎬 MOVIE 페이지
- 검색 기능:
    - 정확한 영화 제목 일치 시 검색 가능 (옵션).
- 장르별 영화 필터링 (드롭다운 메뉴 사용).
- 카테고리별 영화 나열:
    - 최신 영화
    - 인기 영화
    - 개봉 예정 영화
- 각 카테고리에 "더보기" 버튼으로 영화 리스트를 추가적으로 탐색.

#### 🎥 MOVIE-Detail 페이지
- 영화의 상세 정보를 확인 가능:
    - 포스터, 영화 제목, 별점, 감독, 배우, 개봉일, 줄거리.
- 예고편 영상:
    - 유튜브 트레일러 재생 기능.
- 내 카테고리 추가하기:
    - 영화 저장 모달 팝업:
        - 기존 카테고리에 영화 추가 (체크박스).
        - 새로운 카테고리 생성 가능.
- 리뷰 쓰기 버튼:
    - 리뷰 작성 모달 팝업:
        - 제목, 내용, 별점 입력 후 저장.
        - 저장 완료 시 해당 리뷰로 바로 이동.

#### 🗂️ COMMUNITY 페이지
1. 리뷰
    - 영화 검색 및 리뷰 작성:
        - 영화 검색 후 리뷰 작성 버튼을 통해 영화 상세 페이지로 이동.
    - 리뷰 리스트:
        - 최신 리뷰 및 좋아요 순으로 정렬 가능.
        - 각 리뷰는 포스터, 제목, 작성 유저명, 작성일, 좋아요 수, 댓글 수를 표시.
    - 리뷰 상세 페이지:
        - 제목, 작성자 정보, 작성일, 좋아요 수, 댓글 수, 포스터, 리뷰 내용 표시.
        - 좋아요 버튼과 댓글 기능:
            - 댓글 작성, 삭제 기능 포함.
2. 게임
    - 3가지 게임으로 구성:
        - 포스터 보고 영화 제목 맞추기.
        - 명대사 보고 영화 제목 맞추기.
        - 한줄평 보고 영화 제목 맞추기.
    - 게임 페이지:
        - 포스터, 명대사, 혹은 한줄평이 랜덤으로 노출.
        - 텍스트 입력 후 정답 제출 가능.
        - 결과 표시 (정답/오답, 영화 제목).
    - 게임 결과 페이지:
        - 맞춘 개수와 적립된 포인트 표시.
        - "돌아가기" 버튼과 "랭크 확인하기" 버튼 제공.
3. 랭크
    - 사용자 포인트 기반 랭킹 시스템:
        - 1~3위는 금, 은, 동 메달 이미지 표시.
        - 각 사용자 정보(프로필 사진, 이름, 포인트, 게시물 수, 좋아요 수, 팔로워 수) 표시.

#### 👤 프로필 페이지
- 유저 정보:
        - 프로필 사진, 랭크, 유저명, 팔로워/팔로잉 수, 게시글 수, 랭크 등급, 좋아요 수.
- 카테고리 관리:
    - 각 카테고리에 포함된 영화 리스트를 모달로 표시.
    - 카테고리 추가 버튼:
        - 카테고리 이름 입력 및 저장 기능.
- 영화 썸네일과 제목 표시:
    - 클릭 시 해당 영화 상세 페이지로 이동.

### 🛠️ 제작 과정
1. 초기 기획
    - 주요 기능 설계:
        - 영화 탐색, 리뷰 작성, 게임, 랭킹 시스템.
    - UI/UX 설계:
        - 직관적이고 현대적인 레이아웃 구성.
2. 기술 스택 선정
    - Vue.js: 컴포넌트 기반 UI 개발.
    - Django REST Framework: RESTful API 구축.
    - TMDB API: 영화 데이터 제공.
3. 구현 과정
    - 게임 쿨타임: localStorage를 활용하여 게임 반복 플레이 제한.
    - 배경 이미지 동적 로드: 특정 페이지에서만 배경 포스터를 동적으로 설정.
    - 리뷰 작성: 모달 기반 리뷰 작성 및 즉시 반영.
    - 표시 오류 해결: CSS로 텍스트 넘침, 줄바꿈 문제 해결.
4. 테스트 및 배포
    - 로컬 및 클라우드 환경에서 테스트.
    - Vercel과 AWS EC2를 사용해 프론트엔드와 백엔드 배포.

### ⚙️ 기술 스택
#### 프론트엔드
- Vue.js
- Vue Router
- SCSS/CSS
- Axios

#### 백엔드
- Django
- Django REST Framework (DRF)
- SQLite (로컬 DB)

#### 기타
- TMDB API (영화 데이터)
- Git/GitHub (버전 관리)

### 사용 방법
- [front]
cd front/vue-front
npm install
npm install bootstrap
npm run dev

- [back]
cd back
(py -m venv venv)
source venv/Scripts/activate
pip install -r requirements.txt 
py manage.py makemigrations
py manage.py shell
from rest_framework.authtoken.models import Token
Token.objects.filter(user_id=2).delete()
quit()
py manage.py migrate
python manage.py loaddata movies/fixtures/movies/popular.json movies/fixtures/movies/recent.json movies/fixtures/movies/upcoming.json movies/fixtures/movies/movie_data.json
py manage.py runserver

### 느낀 점
#### 팀장 하건수(로그인, 홈, 리뷰, 랭크)

#### 팀원 강혜경(영화, 게임, 카테고리, 프로필)
Movie Monster를 개발하면서 다양한 기능을 구현하고, 사용자 경험을 개선하면서 웹 개반 전반에 대한 깊은 이해를 얻게 되었습니다.
##### 🤔 힘들었던 부분
1. 🎥 영화(Movie)부분
- YouTube API로 트레일러 영상 불러오기
    - 트레일러 영상을 제공하기 위해 YouTube API를 사용했지만, API 응답에서 올바른 영상을 추출하는 과정이 쉽지 않았습니다. 영화별로 정확한 트레일러 영상을 가져오기 위해 검색 키워드와 API 파라미터를 조정해야 했으며, 이를 통해 사용자가 원하는 영상을 최대한 빠르고 정확히 제공하도록 노력했습니다.
- 사용자별 카테고리에 영화 저장, 수정, 삭제
    - 사용자 맞춤형 카테고리 관리 기능은 유저별로 데이터를 저장하는 것과 모달 내에서 동적으로 카테고리를 생성하거나 영화 목록을 수정하는 기능을 구현하는 데 많은 시간이 소요되었습니다.

2. 🕹️ 게임(Game) 부분
- 무한반복 방지를 위한 쿨타임 구현
    - 사용자가 게임을 무제한으로 반복하지 않도록 제한 시간을 구현하는 과정에서 localStorage를 활용했습니다. 그러나, 브라우저 간 데이터 동기화나 비정상적인 상황(예: 브라우저 종료 후 재접속)에서도 쿨타임이 유지되도록 하는 것이 쉽지 않았습니다. 이를 해결하기 위해 시간 계산 로직과 데이터 상태 관리 방식을 설계했습니다.

3. 📊 랭크 및 프로필 페이지
- UX/UI 최적화를 위한 CSS 작업
    - 사용자 랭킹과 프로필 페이지의 디자인을 사용자 친화적으로 만드는 데 많은 시간이 걸렸습니다. 랭킹 테이블에서 콘텐츠가 화면 너비에 따라 깨지지 않도록 반응형 디자인을 구현하거나, 프로필에서 유저 데이터를 보기 쉽게 배치하는 데 CSS 레이아웃을 세심하게 다뤄야 했습니다. 여러 브라우저에서 동일한 UI/UX를 유지하기 위해 CSS 그리드, 플렉스박스, 애니메이션을 활용하여 최적화 작업을 반복적으로 수행했습니다.

##### ✨ 배운 점
1. API 활용 능력
YouTube API를 통해 트레일러 영상을 불러오면서 API의 문서를 읽고 적절한 엔드포인트와 파라미터를 선택하는 능력이 크게 향상되었습니다. API 응답 데이터가 예상과 다를 때 디버깅하고, 여러 시도를 통해 원하는 데이터를 정확히 가져오는 경험은 실무에서도 매우 중요한 기술임을 깨달았습니다.

2. 상태 관리와 데이터 설계
사용자별 카테고리 관리 기능을 통해 복잡한 데이터 구조를 다루고 상태를 관리하는 방법을 배웠습니다. 동적인 데이터 추가, 수정, 삭제가 필요한 경우, 프론트엔드에서의 상태 관리와 백엔드 API 호출의 조화를 이루는 것이 얼마나 중요한지를 경험했습니다.

3. UX 중심의 CSS 최적화
랭킹 페이지와 프로필 페이지에서 사용자 경험을 극대화하기 위해 CSS를 세밀하게 다루는 법을 익혔습니다. 레이아웃이 반응형으로 유지되도록 하고, UI의 직관성을 높이기 위해 요소 간의 간격, 색상 대비, 애니메이션 등을 조정하는 과정에서 CSS의 깊은 이해가 필요하다는 것을 느꼈습니다.

4. 비동기 로직과 상태 유지
게임 쿨타임 기능을 구현하면서 localStorage와 같은 클라이언트 저장소를 효율적으로 활용하는 방법과, 이를 통해 상태를 유지하는 비동기 로직 설계에 익숙해졌습니다. 시간 기반 로직을 구현하며, 예외 상황(브라우저 종료, 데이터 조작 등)을 고려해 안정적인 상태 관리를 하는 방법도 배웠습니다.

##### 🧠 프로젝트를 통해 얻은 인사이트
1. 사용자 맞춤형 서비스의 중요성
유저별 카테고리 관리와 랭킹 기능을 통해 사용자 경험을 개인화할 때 사용자의 흥미를 끌고 유지할 수 있다는 것을 배웠습니다. 단순히 콘텐츠를 제공하는 것을 넘어, 사용자가 적극적으로 참여하고 자신의 데이터에 영향을 미칠 수 있는 기능이 서비스의 가치를 높인다는 것을 깨달았습니다.

2. 복잡한 기능은 단순한 인터페이스로 제공해야 한다
게임 쿨타임이나 리뷰 작성 모달과 같은 기능은 구현 자체가 복잡했지만, 사용자에게는 가능한 한 단순하고 직관적인 인터페이스를 제공해야 한다는 것을 배웠습니다. 복잡한 기능일수록 사용자 입장에서 불편함이 없어야 한다는 점을 염두에 두고 설계했습니다.

3. 서비스 확장성을 고려한 설계
트레일러 영상 불러오기, 랭킹 시스템, 카테고리 관리 등을 구현하면서 미래의 확장성을 고려하는 설계의 중요성을 느꼈습니다. 예를 들어, 카테고리 관리 기능은 영화 외에 다른 콘텐츠를 추가할 수도 있도록 설계했고, 랭킹 시스템은 포인트 외에도 좋아요, 리뷰 수 등 다른 기준으로 확장할 수 있도록 유연하게 구현했습니다.

4. 디자인과 기술의 균형
UI/UX와 기능 구현은 서로 밀접하게 연결되어 있음을 배웠습니다. 사용자 경험을 고려한 디자인은 서비스의 신뢰도를 높이고, 기술적으로 견고한 백엔드와 프론트엔드 구현은 안정성을 더합니다. 이 둘의 균형을 맞추는 것이 성공적인 서비스를 만드는 핵심이라는 것을 깨달았습니다.

