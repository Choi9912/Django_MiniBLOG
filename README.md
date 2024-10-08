# Django_InstaBLOG

## 프로젝트 개요
이 프로젝트는 Django를 사용하여 개발된 기능이 풍부한 블로그 플랫폼입니다. 인스타그램의 감성에 맞춰 디자인된 사용자 친화적인 인터페이스와 다양한 소셜 기능을 통해, 글쓰기와 커뮤니티 활동을 더욱 매력적이고 즐겁게 경험할 수 있도록 지원합니다. 트렌디한 비주얼과 직관적인 사용자 경험을 바탕으로, 사용자들이 자신의 이야기를 스타일리시하게 표현하고, 소통하며, 커뮤니티를 구축할 수 있는 공간을 제공합니다.

## WBS 
![Untitled diagram-2024-08-31-052548](https://github.com/user-attachments/assets/78fc73a4-02ff-45cc-bc6f-c7a2e2fe0ba2)



## WireFrame
| Image 1 | Image 2 | Image 3                                                                                                                                      |
|---------|---------|----------------------------------------------------------------------------------------------------------------------------------------------|
| <img src="https://github.com/user-attachments/assets/c740b288-8830-4082-bee4-9d8aa13ba3ec" width="300" alt="Image 1"> | <img src="https://github.com/user-attachments/assets/9b5258c0-0396-4b0a-b368-cdfba157fec6" width="300" alt="Image 2"> | <img src="https://github.com/user-attachments/assets/b035bec1-c9da-41cb-b09b-7f115b0eb7f0" width="300" height=430 alt="Image 3">             |
| <img src="https://github.com/user-attachments/assets/ddb811be-803a-42e8-92d8-edd43cee4df1" width="300" alt="Image 4"> | <img src="https://github.com/user-attachments/assets/4b82e9ed-ba11-44db-a555-9c13265e7bbd" width="300" alt="Image 5"> | <img src="https://github.com/user-attachments/assets/0c91d59a-216f-4c5b-aa11-eac7cbeb68b1" width="300" height=450 alt="Instablog Wireframe"> |
| <img src="https://github.com/user-attachments/assets/bb226c6d-fe9d-4734-94d5-4c4fa7ac54fb" width="300" alt="Additional Image"> | |                                                                                                                                              |
## 기술 스택
**Enviroment**  

<img src="https://img.shields.io/badge/Visual Studio Code-2F80ED?style=for-the-badge&logo=VSC&logoColor=white">  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">


**Frontend**

<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css3-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white"> 

**Backend**

<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white">

**Infrastructure & Deployment**

<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"> <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=Nginx&logoColor=white"> <img src="https://img.shields.io/badge/amazonec2-000000?style=for-the-badge&logo=amazonec2&logoColor=white">
<img src="https://img.shields.io/badge/redis-FF4438?style=for-the-badge&logo=Django&logoColor=white"> 

## 설치 방법
```
0. 저장소 클론
git clone https://github.com/Choi9912/Django_MiniBLOG.git

1. 가상 환경 설정
python3 -m venv venv
source venv/bin/activate

2. 의존성 설치
pip install -r requirements.txt

3. 데이터베이스 마이그레이션
python manage.py makemigrations
python manage.py migrate

4. 서버 실행
python manage.py runserver
```


## 프로젝트 기능 목록 📋

### 1. 사용자 인증 및 프로필 👤

- 🔐 커스텀 로그인 뷰 
  - allauth 사용하여 카카오톡/네이버 소셜로그인 계정 이용 가능
- ✏️ 프로필 업데이트 기능
- 👀 프로필 상세 보기 (자신 및 다른 사용자)
- 🤝 팔로우/언팔로우 기능

### 2. 게시물 관리 📝

- 📜 게시물 목록 보기 (정렬 옵션: 최신순, 좋아요순, 조회수순)
- 🔍 게시물 상세 보기 
- ✨ 게시물 생성, 수정, 삭제 (GPT활용한 제목 자동완성 기능 가능)
- 🔎 게시물 검색 (제목, 태그, 카테고리, 전체)
- 🏆 인기 게시물 및 주간 랭킹 표시

### 3. 댓글 시스템 💬

- ✍️ 댓글 작성, 수정, 삭제
- 🔄 대댓글 기능 
  - 재귀적 호출을 통한 깊이 제한없이 대댓글 생성가능

### 4. 카테고리 및 태그 🏷️

- 📁 카테고리 목록 및 카테고리별 게시물 보기
- 🔖 태그 목록 및 태그별 게시물 보기
- ℹ️ 태그 상세 정보 페이지

### 5. 사용자 상호작용 🤝

- 👍 게시물 좋아요 기능
- 🔗 게시물 공유 기능

### 7. 채팅 기능 💬

- 💬 채팅 기능
  - WebSocket & Daphne & Redis

### 8. 대시보드 📊

- 📈 사용자별 대시보드 (게시물 수, 총 조회수, 총 좋아요 수, 팔로워 수)

### 9. 부가 기능 🛠️

- 🧭 사이드바에 카테고리 및 태그 목록 표시
- 📄 페이지네이션 (게시물 목록, 검색 결과 등)
- 👁️ 조회수 자동 증가 (게시물 상세 보기 시)

### 10. 보안 및 권한 관리 🔒

- 🚫 로그인 필요 기능에 대한 접근 제어
- 🔐 작성자만 수정/삭제 가능하도록 권한 체크

### 11. 성능 최적화 🚀

- 💪 데이터베이스 쿼리 최적화 (annotate, aggregate 사용)
  - `aggregate`와 `annotate`는 Django ORM에서 제공하는 쿼리셋 메소드
  - 데이터 집계 또는 쿼리셋에 계산 필드를 추가하는데 사용
- 🏎️ 트랜잭션과 F() 표현식을 활용한 안전하고 효율적인 조회수 증가 처리
  - 데이터베이스 트랜잭션을 보장하여 동시성 문제 방지


## 엔티티 관계 다이어그램 ERD
![Untitled diagram-2024-09-01-063203](https://github.com/user-attachments/assets/f694453e-9ed7-4044-8c0b-32df6a155b2d)

- 주요 특징
1. Profile 모델이 사용자 정보의 중심이 되어 다른 모든 모델과 관계를 맺고 있습니다.
2. Conversation 모델은 여러 Profile(참여자)과 연결될 수 있고, 각 Profile도 여러 Conversation에 참여할 수 있습니다.
3. 댓글(Comment)은 여전히 자기 참조 관계를 가져 대댓글 구조를 표현합니다.
4. 좋아요(Like)와 팔로워(Follower) 관계도 Profile 모델을 중심으로 표현됩니다.

## 블로그 앱 URL 구성
## 프로젝트 URL 구성
| 기능 | URL 패턴 | 뷰 | 설명 |
|------|---------|-----|--------|
| **메인** | `/` | `PostListView.as_view()` | 게시물 목록 (홈) |
| **인증** | `/accounts/login/` | `allauth.account.views.LoginView.as_view()` | 로그인 |
| | `/accounts/logout/` | `allauth.account.views.LogoutView.as_view()` | 로그아웃 |
| | `/accounts/signup/` | `allauth.account.views.SignupView.as_view()` | 회원가입 |
| | `/accounts/password/reset/` | `allauth.account.views.PasswordResetView.as_view()` | 비밀번호 재설정 |
| **프로필** | `/profile/update/` | `ProfileUpdateView.as_view()` | 프로필 수정 |
| | `/profile/<str:username>/` | `ProfileDetailView.as_view()` | 프로필 조회 |
| **대시보드** | `/dashboard/` | `user_dashboard` | 사용자 대시보드 |
| **게시물** | `/post/<int:pk>/` | `PostDetailView.as_view()` | 게시물 상세 |
| | `/post/new/` | `PostCreateView.as_view()` | 게시물 생성 |
| | `/post/<int:pk>/edit/` | `PostUpdateView.as_view()` | 게시물 수정 |
| | `/post/<int:pk>/delete/` | `PostDeleteView.as_view()` | 게시물 삭제 |
| | `/post/<int:pk>/like/` | `PostLikeToggleView.as_view()` | 게시물 좋아요 |
| | `/search/` | `PostSearchView.as_view()` | 게시물 검색 |
| **댓글** | `/post/<int:post_pk>/comment/new/` | `CommentCreateView.as_view()` | 댓글 생성 |
| | `/comment/<int:pk>/edit/` | `CommentUpdateView.as_view()` | 댓글 수정 |
| | `/comment/<int:pk>/delete/` | `CommentDeleteView.as_view()` | 댓글 삭제 |
| | `/comment/<int:comment_pk>/reply/` | `ReplyCreateView.as_view()` | 답글 생성 |
| | `/reply/<int:pk>/update/` | `ReplyUpdateView.as_view()` | 답글 수정 |
| | `/reply/<int:pk>/delete/` | `ReplyDeleteView.as_view()` | 답글 삭제 |
| **카테고리** | `/categories/` | `CategoryListView.as_view()` | 카테고리 목록 |
| | `/category/<str:slug>/` | `CategoryPostListView.as_view()` | 카테고리별 게시물 |
| **태그** | `/tags/` | `TagListView.as_view()` | 태그 목록 |
| | `/tag/<str:slug>/` | `TagPostListView.as_view()` | 태그별 게시물 |
| **사용자 상호작용** | `/follow/<str:username>/` | `FollowToggleView.as_view()` | 팔로우/언팔로우 |
| | `/share/<int:post_id>/` | `share_post` | 게시물 공유 |
| **채팅** | `/chat/` | `ConversationListView.as_view()` | 대화 목록 표시 |
| | `/chat/<str:room_name>/` | `RoomView.as_view()` | 특정 채팅방 표시 |
| | `/chat/start/` | `StartConversationView.as_view()` | 새로운 대화 시작 |
| | `/chat/start/<str:username>/` | `StartConversationView.as_view()` | 지정된 사용자와 새 대화 시작 |
| | `/chat/<int:room_id>/messages/` | `get_chat_messages` | 특정 채팅방의 메시지 조회 |
| | `/chat/delete/<int:pk>/` | `DeleteConversationView.as_view()` | 특정 대화 삭제 |
## 시연
| Accounts | Blog | 
|------|---------|
| ![Blog-Posts-Chrome-2024-08-31-14-31-04](https://github.com/user-attachments/assets/f214b60f-e6a6-4efe-b93d-ea862bcf3457) | ![Blog-Posts-Chrome-2024-08-31-14-33-09](https://github.com/user-attachments/assets/8f34f5a0-0766-4067-9316-7829679ed337) 

| Comments | Chat |
|------|------|
| ![굳_-성공을-위한-테크의-힘_-Chrome-2024-08-31-14-34-46](https://github.com/user-attachments/assets/e4f0af6f-a3fe-428b-8236-bd558a5769f4) | ![Animation](https://github.com/user-attachments/assets/9b01b484-0523-41f0-87bd-96bb0b24cc38)
 |

## 기술적 도전과 해결 방안

1. **소셜 로그인 계정 도입**

- 도전: 여러 소셜 로그인 제공자의 통합 및 커스터 마이징 하고 싶었습니다.

- 해결 방안:
  - Django allauth: 사용자 인증 및 권한 관리를 Django allauth를 통해 표준화하고, 추가적인 커스텀 로직을 적용했습니다.

2. **재귀적 호출 대답글 작성**
- 도전 : 1단계적인 댓글 기능 구현했지만, 추가적으로 반복되는 답글 기능에 있어서 어려움을 겪고 있었습니다.
- 해결 방안 :
  -  decision tree의 max_depth 파라미터에 영감을 받음.
    - 모델 : parent_comment와 depth 필드 추가 
    - 뷰 : ReplyCreateView에서 depth 관리
  
3. **채팅 기능**
- 도전 : 동기적 채팅을 구현했지만 실시간 통신과 확장성을 위해 비동기적 채팅을 구현하려 하였습니다.
- 해결 방안:
  - Websocket : Django Channels 라이브러리를 활용하여 WebSocket 연결 구현
  - Daphne & Redis :
    - Daphne: ASGI 서버로 WebSocket 요청 처리
    - Redis: 채널 레이어로 사용하여 여러 서버 인스턴스 간 메시지 브로딩캐스팅

4. **스케일링 및 배포**
- 도전: 웹 서버의 스케일링 및 안정적인 배포가 필요했습니다.
- 해결 방안:
    - Docker: 애플리케이션을 컨테이너화하여 배포 및 환경 설정을 표준화했습니다.
    - Nginx 로드 밸런싱: Nginx를 로드 밸런서로 사용하여 여러 서버에 요청을 분산시키고, 애플리케이션의 확장성을 보장했습니다.
    - AWS EC2: AWS EC2를 사용하여 인프라를 확장하고 안정적인 서비스를 제공했습니다.

