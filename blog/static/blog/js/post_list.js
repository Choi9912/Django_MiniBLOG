document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-button').forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const likeUrl = `/blog/like/${postId}/`;
            const likesCountElement = this.nextElementSibling;
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            fetch(likeUrl, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({}),
                redirect: 'manual'  // 추가된 부분
            })
            .then(response => {
                if (response.type === 'opaqueredirect') {
                    throw new Error('login_required');
                }
                if (!response.ok) {
                    return response.json().then(data => {
                        if (data.error === 'login_required') {
                            throw new Error('login_required');
                        }
                        throw new Error('HTTP error ' + response.status);
                    });
                }
                return response.json();
            })
            .then(data => {
                likesCountElement.textContent = `${data.likes_count} `;
                if (data.liked) {
                    this.classList.add('liked');
                } else {
                    this.classList.remove('liked');
                }
            })
            .catch(error => {
                if (error.message === 'login_required') {
                    if (confirm('로그인이 필요합니다. 로그인 페이지로 이동하시겠습니까?')) {
                        window.location.href = '/accounts/login/';
                    }
                } else {
                    console.error('Error:', error);
                }
            });
        });
    });
});