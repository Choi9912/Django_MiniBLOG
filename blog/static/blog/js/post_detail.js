document.addEventListener('DOMContentLoaded', function() {
  const likeButton = document.querySelector('.like-btn');
  const likesCountElement = document.querySelector('.like-count');
  
  if (likeButton) {
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
              likesCountElement.textContent = data.likes_count;
              if (data.liked) {
                  likeButton.classList.add('liked');
                  likeButton.querySelector('i').classList.remove('far');
                  likeButton.querySelector('i').classList.add('fas');
              } else {
                  likeButton.classList.remove('liked');
                  likeButton.querySelector('i').classList.remove('fas');
                  likeButton.querySelector('i').classList.add('far');
              }
          })
          .catch(error => {
              console.error('Error:', error);
              alert('Failed to update like. Please try again later.');
          });
      });
  }
  // Share button functionality
  $('.share-btn').click(function(e) {
    e.preventDefault();
    window.location.href = sharePostUrl;
  });

  // Follow button functionality
  $('.follow-btn').click(function() {
    var userId = $(this).data('user-id');
    var button = $(this);
    $.post('/follow/' + userId + '/', function(data) {
      if (data.following) {
        button.text('Unfollow');
      } else {
        button.text('Follow');
      }
    });
  });
});