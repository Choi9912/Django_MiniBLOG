document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-button').forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const likeUrl = `/blog/like/${postId}/`;  // URL을 올바르게 설정했는지 확인하세요
            const likesCountElement = this.nextElementSibling;
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            fetch(likeUrl, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 401) {
                        throw new Error('login_required');
                    }
                    throw new Error('HTTP error ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (data.error === 'login_required') {
                    throw new Error('login_required');
                }
                likesCountElement.textContent = `${data.likes_count} `;
                if (data.liked) {
                    this.classList.add('liked');
                } else {
                    this.classList.remove('liked');
                }
            })
            .catch(error => {
                if (error.message === 'login_required') {
                    alert('로그인이 필요합니다. 로그인 페이지로 이동합니다.');
                    window.location.href = '/accounts/login/';  // 로그인 페이지 URL을 적절히 수정하세요
                } else {
                    console.error('Error:', error);
                }
            });
        });
    });
});