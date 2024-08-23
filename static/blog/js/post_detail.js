document.addEventListener('DOMContentLoaded', function() {
  // 좋아요 버튼 처리
  const likeButtons = document.querySelectorAll('.like-btn');
  
  likeButtons.forEach(likeButton => {
    likeButton.addEventListener('click', function(e) {
      e.preventDefault();
      const postId = this.dataset.postId;
      const url = `/post/${postId}/like/`;

      // CSRF 토큰 가져오기
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      fetch(url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrftoken
        }
      })
      .then(response => response.json())
      .then(data => {
        const likesCountElement = this.querySelector('.like-count');
        likesCountElement.textContent = data.likes_count;
        if (data.liked) {
          this.classList.add('liked');
          this.querySelector('i').classList.remove('far');
          this.querySelector('i').classList.add('fas');
        } else {
          this.classList.remove('liked');
          this.querySelector('i').classList.remove('fas');
          this.querySelector('i').classList.add('far');
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
});
