# Django_InstaBLOG

## 기능

- **회원가입 및 로그인** :
사용자는 allauth 사용하여 플랫폼에 접근할 수 있습니다. 로그인 후, 사용자는 자신의 프로필을 관리하고 블로그 포스트 및 댓글 작성 등의 기능을 사용할 수 있습니다.

- **프로필 관리** :
사용자는 프로필을 설정하고 업데이트할 수 있으며, 기본 프로필 이미지가 제공됩니다.

- **게시판 기능** :
사용자는 작성한 블로그 포스트를 게시하고, 다른 사용자의 포스트를 열람할 수 있습니다.

- **카테고리 및 태그** :
포스트는 카테고리와 태그를 통해 구분할 수 있으며, 카테고리와 태그에 따라 포스트를 필터링할 수 있습니다.

- **댓글 기능** :
사용자는 포스트에 댓글을 작성하고, 댓글을 수정 및 삭제할 수 있습니다.

- **댓글 답글 기능** :
사용자는 댓글에 답글을 작성할 수 있습니다.

- **좋아요 기능** : 
포스트와 댓글에 좋아요를 표시할 수 있습니다.


## 엔티티 관계 다이어그램 ERD
![image](https://github.com/user-attachments/assets/79c10dba-dffb-4883-97bc-d927446913f4)

## 블로그 앱 URL 구성
| **URL 패턴**                                    | **뷰**                           | **이름**                | **설명**                                             |
|-------------------------------------------------|----------------------------------|-------------------------|------------------------------------------------------|
| `/`                                             | `PostListView`                    | `post_list`             | 모든 블로그 포스트의 목록을 표시합니다.              |
| `/profile/`                                    | `ProfileView`                     | `profile_view`          | 사용자의 프로필을 표시합니다.                       |
| `/profile/edit/`                               | `ProfileUpdateView`               | `profile_update`        | 사용자가 자신의 프로필 정보를 업데이트할 수 있는 폼을 제공합니다. |
| `/post/<int:pk>/`                              | `PostDetailView`                  | `post_detail`           | 특정 포스트의 세부 정보를 표시합니다. (`pk`로 식별) |
| `/post/new/`                                   | `PostCreateView`                  | `post_create`           | 새 포스트를 작성할 수 있는 폼을 제공합니다.          |
| `/post/<int:pk>/edit/`                         | `PostUpdateView`                  | `post_update`           | 기존 포스트를 수정할 수 있는 폼을 제공합니다. (`pk`로 식별) |
| `/post/<int:pk>/delete/`                       | `PostDeleteView`                  | `post_delete`           | 특정 포스트를 삭제합니다. (`pk`로 식별)             |
| `/login/`                                      | `CustomLoginView`                 | `account_login`         | 사용자 로그인을 위한 폼을 제공합니다.              |
| `/search/`                                     | `PostSearchView`                  | `post_search`           | 포스트를 검색할 수 있는 기능을 제공합니다.         |
| `/post/<int:post_pk>/comment/new/`              | `CommentCreateView`               | `comment_create`        | 특정 포스트에 대한 새 댓글을 작성할 수 있는 폼을 제공합니다. (`post_pk`로 식별) |
| `/comment/<int:pk>/edit/`                      | `CommentUpdateView`               | `comment_update`        | 기존 댓글을 수정할 수 있는 폼을 제공합니다. (`pk`로 식별) |
| `/comment/<int:pk>/delete/`                    | `CommentDeleteView`               | `comment_delete`        | 특정 댓글을 삭제합니다. (`pk`로 식별)              |
| `/post/<int:pk>/like/`                         | `PostLikeToggleView`              | `post_like_toggle`      | 특정 포스트의 좋아요 상태를 토글합니다. (`pk`로 식별) |
| `/comment/<int:pk>/like/`                      | `CommentLikeToggleView`           | `comment_like_toggle`   | 특정 댓글의 좋아요 상태를 토글합니다. (`pk`로 식별) |
| `/comment/<int:comment_pk>/reply/new/`          | `ReplyCreateView`                 | `reply_create`          | 특정 댓글에 대한 답글을 작성할 수 있는 폼을 제공합니다. (`comment_pk`로 식별) |
| `/categories/`                                 | `CategoryListView`                | `category_list`         | 모든 카테고리의 목록을 표시합니다.                  |
| `/tags/`                                       | `TagListView`                     | `tag_list`              | 모든 태그의 목록을 표시합니다.                      |
| `/category/<str:slug>/`                        | `CategoryPostListView`            | `category_posts`        | 특정 카테고리에 속하는 포스트를 표시합니다. (`slug`로 식별) |
| `/tag/<str:slug>/`                             | `TagPostListView`                 | `tag_posts`             | 특정 태그와 연관된 포스트를 표시합니다. (`slug`로 식별) |
