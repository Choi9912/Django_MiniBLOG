document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded event fired');

    // Initialize Select2 for tags
    initializeTagsField();

    // Title suggestion functionality
    initializeTitleSuggestion();

    function initializeTagsField() {
        const tagsField = document.getElementById('id_tags');
        if (tagsField) {
            $(tagsField).select2({
                tags: true,
                tokenSeparators: [',', ' '],
                placeholder: "Enter tags",
            });
        } else {
            console.warn('Tags field not found. Element ID: id_tags');
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const autoCompleteBtn = document.getElementById('autoCompleteBtn');
    const categorySelect = document.querySelector('select[name="category"]');
    const tagsInput = document.querySelector('input[name="tags"]');
    const titleInput = document.querySelector('input[name="title"]');

    autoCompleteBtn.addEventListener('click', function() {
        const category = categorySelect.options[categorySelect.selectedIndex].text;
        const tags = tagsInput.value;

        if (!category || !tags) {
            alert('카테고리와 태그를 먼저 입력해주세요.');
            return;
        }

        const url = 'https://open-api.jejucodingcamp.workers.dev/';
        const data = [
            {
                "role": "system",
                "content": "당신은 블로그 포스트 제목을 생성하는 AI 어시스턴트입니다."
            },
            {
                "role": "user",
                "content": `다음 카테고리와 태그를 사용하여 흥미로운 블로그 포스트 제목을 생성해주세요. 
                
                카테고리: "${category}", 태그: "${tags}". 제목은 간결하고 매력적이어야 합니다.`
            }
        ];

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
            redirect: "follow",
        })
        .then((res) => res.json())
        .then((res) => {
            const generatedTitle = res.choices[0].message.content;
            titleInput.value = generatedTitle;
        })
        .catch((err) => {
            console.error('Error:', err);
            alert('제목 자동완성 중 오류가 발생했습니다. 다시 시도해주세요.');
        });
    });
});