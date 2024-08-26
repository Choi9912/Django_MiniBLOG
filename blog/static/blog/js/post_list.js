document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const url = this.action;
            const likeButton = this.querySelector('.like-button');
            const likesCountElement = this.nextElementSibling;

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
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
                    alert('로그인을 해주세요');
                } else {
                    likesCountElement.textContent = `${data.likes_count} likes`;
                    if (data.liked) {
                        likeButton.classList.add('liked');
                    } else {
                        likeButton.classList.remove('liked');
                    }
                }
            })
            .catch(error => {
                if (error.message === 'login_required') {
                    alert('로그인을 해주세요');
                } else {
                    console.error('Error:', error);
                }
            });
        });
    });
});