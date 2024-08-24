
document.addEventListener('DOMContentLoaded', function() {
  // 좋아요 버튼 처리
  document.querySelectorAll('.like-form').forEach(function(form) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const url = this.action;
        const likeButton = this.querySelector('.like-btn');
        const heartIcon = likeButton.querySelector('i');
        const likeCountElement = likeButton.querySelector('.like-count');

        fetch(url, {
            method: 'POST',
            body: new FormData(this),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            likeCountElement.textContent = data.likes_count;
            if (data.liked) {
                likeButton.classList.add('liked');
                heartIcon.classList.remove('far');
                heartIcon.classList.add('fas');
            } else {
                likeButton.classList.remove('liked');
                heartIcon.classList.remove('fas');
                heartIcon.classList.add('far');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to update like. Please try again later.');
        });
    });
});

  // 공유 버튼 기능
  $('.share-btn').click(function(e) {
    e.preventDefault();
    window.location.href = sharePostUrl;
  });

  // 팔로우 버튼 기능
  $('.follow-btn').click(function() {
    var userId = $(this).data('user-id');
    var button = $(this);
    $.post(`/follow/${userId}/`, function(data) {
      if (data.following) {
        button.text('Unfollow');
      } else {
        button.text('Follow');
      }
    });
  });
});$(document).ready(function() {
  // 대댓글 폼 생성
  $(document).on('click', '.reply-btn', function() {
      var commentContainer = $(this).closest('.comment-container');
      var commentId = commentContainer.data('comment-id');
      var replyForm = `
          <form class="mt-2 reply-form">
              <input type="hidden" name="parent_comment_id" value="${commentId}">
              <div class="input-group">
                  <input type="text" name="content" class="form-control" placeholder="Add a reply..." required>
                  <div class="input-group-append">
                      <button type="submit" class="btn btn-outline-primary btn-sm">Reply</button>
                  </div>
              </div>
          </form>
      `;
      $(this).after(replyForm);
      $(this).hide();
  });

  // Ajax를 사용한 댓글 제출
  $(document).on('submit', '#main-comment-form, .reply-form', function(e) {
      e.preventDefault();
      var form = $(this);
      $.ajax({
          url: commentCreateUrl,
          type: 'POST',
          data: form.serialize(),
          headers: {
              "X-CSRFToken": csrfToken
          },
          success: function(response) {
              var newComment = $(response.html);
              if (response.parent_id) {
                  // 대댓글인 경우
                  var parentContainer = $('[data-comment-id="' + response.parent_id + '"]');
                  var repliesContainer = parentContainer.find('.replies-container');
                  if (repliesContainer.length === 0) {
                      parentContainer.append('<div class="replies-container"></div>');
                      repliesContainer = parentContainer.find('.replies-container');
                  }
                  repliesContainer.append(newComment);
                  parentContainer.find('> .reply-btn').show();
                  parentContainer.find('> .reply-form').remove();
              } else {
                  // 최상위 댓글인 경우
                  $('#comments-container').append(newComment);
              }
              form.find('input[name="content"]').val('');
          },
          error: function(xhr, status, error) {
              console.error("Error submitting comment:", error);
          }
      });
  });

  // 기존의 다른 이벤트 핸들러들 (좋아요, 공유, 팔로우 등)은 그대로 유지
});