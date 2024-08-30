document.addEventListener('DOMContentLoaded', function() {
    const followToggle = document.querySelector('.follow-toggle');
    if (followToggle) {
        followToggle.addEventListener('click', function() {
            const username = this.dataset.username;
            const isOwnProfile = document.body.classList.contains('own-profile');
            
            if (isOwnProfile) {
                alert('자기 자신을 팔로우할 수 없습니다.');
                return;
            }
            
            toggleFollow(username, this);
        });
    }
});

function toggleFollow(username, button) {
    fetch(`/accounts/follow/${username}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        button.textContent = data.is_following ? '팔로우 취소' : '팔로우';
        const followerCountElement = document.querySelector('.profile-stats span:nth-child(2) strong');
        if (followerCountElement) {
            followerCountElement.textContent = data.follower_count;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('팔로우 토글 중 오류가 발생했습니다.');
    });
}

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