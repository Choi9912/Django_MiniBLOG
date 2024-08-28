# Django_InstaBLOG

## 프로젝트 개요
이 프로젝트는 Django를 사용하여 개발된 기능이 풍부한 블로그 플랫폼입니다. 인스타그램의 감성에 맞춰 디자인된 사용자 친화적인 인터페이스와 다양한 소셜 기능을 통해, 글쓰기와 커뮤니티 활동을 더욱 매력적이고 즐겁게 경험할 수 있도록 지원합니다. 트렌디한 비주얼과 직관적인 사용자 경험을 바탕으로, 사용자들이 자신의 이야기를 스타일리시하게 표현하고, 소통하며, 커뮤니티를 구축할 수 있는 공간을 제공합니다.

## WBS 
![image](https://github.com/user-attachments/assets/722eae6b-3f8c-455c-b8d0-cddace51bed1)


## WireFrame
https://www.figma.com/proto/F7hoJXjZ77lYNfIcu6a3Db/Prototyping-in-Figma?node-id=0-1&t=T1vnHxYG4hhLq5Vz-1

## 기술 스택
**Enviroment**  

<img src="https://img.shields.io/badge/Visual Studio Code-2F80ED?style=for-the-badge&logo=VSC&logoColor=white">  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">


**Frontend**

<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css3-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white"> 

**Backend**

<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"> 

**Infrastructure & Deployment**

<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"> <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=Nginx&logoColor=white"> <img src="https://img.shields.io/badge/amazonec2-000000?style=for-the-badge&logo=amazonec2&logoColor=white">

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

- 🔐 커스텀 로그인 뷰 (AllAuth 사용)
- ✏️ 프로필 업데이트 기능
- 👀 프로필 상세 보기 (자신 및 다른 사용자)
- 🤝 팔로우/언팔로우 기능

### 2. 게시물 관리 📝

- 📜 게시물 목록 보기 (정렬 옵션: 최신순, 좋아요순, 조회수순)
- 🔍 게시물 상세 보기 (마크다운 지원, 태그 링크 자동 생성)
- ✨ 게시물 생성, 수정, 삭제(GPT활용한 제목 자동완성 기능)
- 🔎 게시물 검색 (제목, 태그, 카테고리, 전체)
- 🏆 인기 게시물 및 주간 랭킹 표시

### 3. 댓글 시스템 💬

- ✍️ 댓글 작성, 수정, 삭제
- 🔄 대댓글 기능 

### 4. 카테고리 및 태그 🏷️

- 📁 카테고리 목록 및 카테고리별 게시물 보기
- 🔖 태그 목록 및 태그별 게시물 보기
- ℹ️ 태그 상세 정보 페이지

### 5. 사용자 상호작용 🤝

- 👍 게시물 좋아요 기능
- 🔗 게시물 공유 기능

### 6. 대시보드 📊

- 📈 사용자별 대시보드 (게시물 수, 총 조회수, 총 좋아요 수, 팔로워 수)

### 7. 부가 기능 🛠️

- 🧭 사이드바에 카테고리 및 태그 목록 표시
- 📄 페이지네이션 (게시물 목록, 검색 결과 등)
- 👁️ 조회수 자동 증가 (게시물 상세 보기 시)

### 8. 보안 및 권한 관리 🔒

- 🚫 로그인 필요 기능에 대한 접근 제어
- 🔐 작성자만 수정/삭제 가능하도록 권한 체크

### 9. 성능 최적화 🚀

- 💪 데이터베이스 쿼리 최적화 (annotate, aggregate 사용)
  - `aggregate`와 `annotate`는 Django ORM에서 제공하는 쿼리셋 메소드
  - 데이터 집계 또는 쿼리셋에 계산 필드를 추가하는데 사용
- 트랜잭션과 F() 표현식을 활용한 안전하고 효율적인 조회수 증가 처리
  - 데이터베이스 트랜잭션을 보장하여 동시성 문제 방지


## 엔티티 관계 다이어그램 ERD
![Untitled diagram-2024-08-28-012255](https://github.com/user-attachments/assets/b61dd14f-8102-4c3f-a9c8-20a4de5ef690)


## 블로그 앱 URL 구성
| 기능 | URL 패턴 | 뷰 | 설명 |
|------|---------|-----|------|
| **메인** | `/` | `PostListView.as_view()` | 게시물 목록 (홈) |
| **인증** | `/login/` | `CustomLoginView.as_view()` | 로그인 |
| **프로필** | `/profile/update/` | `ProfileUpdateView.as_view()` | 프로필 수정 |
| | `/profile/<str:username>/` | `ProfileDetailView.as_view()` | 프로필 조회 |
| **대시보드** | `/dashboard/` | `user_dashboard` | 사용자 대시보드 |
| **게시물** | `/post/<int:pk>/` | `PostDetailView.as_view()` | 게시물 상세 |
| | `/post/new/` | `PostCreateView.as_view()` | 게시물 생성 |
| | `/post/<int:pk>/edit/` | `PostUpdateView.as_view()` | 게시물 수정 |
| | `/post/<int:pk>/delete/` | ` PostDeleteView.as_view()` | 게시물 삭제 |
| | `/post/<int:pk>/like/` | `PostLikeToggleView.as_view()` | 게시물 좋아요 |
| | `/search/` | `PostSearchView.as_view()` | 게시물 검색 |
| **댓글** | `/post/<int:post_pk>/comment/new/` | `CommentCreateView.as_view()` | 댓글 생성 |
| | `/comment/<int:pk>/edit/` | `CommentUpdateView.as_view()` | 댓글 수정 |
| | `/comment/<int:pk>/delete/` | `CommentDeleteView.as_view()` | 댓글 삭제 |
| | `/comment/<int:comment_pk>/reply/` | `ReplyCreateView.as_view()` | 답글 생성 |
| | `/reply/<int:pk>/delete/` | `ReplyDeleteView.as_view()` | 답글 삭제 |
| **카테고리** | `/categories/` | `CategoryListView.as_view()` | 카테고리 목록 |
| | `/category/<str:slug>/` | `CategoryPostListView.as_view()` | 카테고리별 게시물 |
| **태그** | `/tags/` | `TagListView.as_view()` | 태그 목록 |
| | `/tag/<str:slug>/` | `TagPostListView.as_view()` | 태그별 게시물 |
| | `/tag/<str:slug>/detail/` | `TagDetailView.as_view()` | 태그 상세 |
| **사용자 상호작용**  | `/follow/<str:username>/` | `FollowToggleView.as_view()` | 팔로우/언팔로우 |
| | `/share/<int:post_id>/` | `share_post` | 게시물 공유 |


