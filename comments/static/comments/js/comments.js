document.addEventListener('DOMContentLoaded', function() {
    const commentSection = document.querySelector('.comments-section');

    commentSection.addEventListener('click', function(e) {
        if (e.target.classList.contains('reply-btn')) {
            const commentId = e.target.dataset.commentId;
            const replyForm = document.getElementById(`reply-form-${commentId}`);
            replyForm.classList.toggle('d-none');
        }

        if (e.target.classList.contains('cancel-reply')) {
            const replyForm = e.target.closest('.reply-form');
            replyForm.classList.add('d-none');
        }
    });

    // 댓글 및 답글 폼 제출 처리
    commentSection.addEventListener('submit', function(e) {
        if (e.target.classList.contains('comment-form')) {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);
            const url = form.action;

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    // 성공적으로 제출되면 페이지를 새로고침합니다.
                    window.location.reload();
                } else {
                    console.error('Form submission failed');
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });
});

// CSRF 토큰을 가져오는 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}