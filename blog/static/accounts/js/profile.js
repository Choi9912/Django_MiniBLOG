document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    const followBtn = document.getElementById('follow-btn');
    if (followBtn) {
        console.log('Follow button found:', followBtn);
        followBtn.addEventListener('click', function() {
            console.log('Follow button clicked');
            const username = this.dataset.username;
            fetch(`/blog/follow/${username}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_following) {
                    this.textContent = 'Unfollow';
                } else {
                    this.textContent = 'Follow';
                }
                document.getElementById('follower-count').textContent = data.follower_count;
            })
            .catch(error => {
                console.error('Error:', error);
                alert('팔로우 처리 중 오류가 발생했습니다. 다시 시도해 주세요.');
            });
        });
    } else {
        console.log('Follow button not found');
    }
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
console.log('Profile page loaded');
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    const followBtn = document.getElementById('follow-btn');
    if (followBtn) {
        console.log('Follow button found:', followBtn);
        followBtn.addEventListener('click', function() {
            console.log('Follow button clicked');
            // 기존의 follow 로직
        });
    } else {
        console.log('Follow button not found');
    }
});