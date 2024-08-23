document.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('.popular-blog-item');

    // 초기화: 로컬 스토리지에서 클릭된 포스트 확인
    items.forEach(item => {
        const id = item.getAttribute('data-id');
        if (localStorage.getItem(clicked_${id})) {
            item.classList.add('clicked');
        }
    });

    // 클릭 이벤트 처리
    items.forEach(item => {
        item.addEventListener('click', () => {
            const id = item.getAttribute('data-id');
            item.classList.add('clicked');
            localStorage.setItem(clicked_${id}, 'true');
        });
    });
});