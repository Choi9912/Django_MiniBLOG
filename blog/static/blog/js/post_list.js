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
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                likesCountElement.textContent = `${data.likes_count} likes`;
                if (data.liked) {
                    likeButton.classList.add('liked');
                } else {
                    likeButton.classList.remove('liked');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});