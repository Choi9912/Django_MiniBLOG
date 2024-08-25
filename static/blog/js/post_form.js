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

    function initializeTitleSuggestion() {
        const titleInput = document.getElementById('id_title');
        const suggestButton = document.getElementById('suggest-title');
        const suggestedTitleDiv = document.getElementById('suggested-title');
        const suggestedTitleText = document.getElementById('suggested-title-text');
        const useSuggestedTitleButton = document.getElementById('use-suggested-title');

        if (titleInput && suggestButton && suggestedTitleDiv && suggestedTitleText && useSuggestedTitleButton) {
            suggestButton.addEventListener('click', function() {
                const title = titleInput.value.trim();
                if (title.length > 0) {
                    fetchSuggestedTitle(title);
                }
            });

            useSuggestedTitleButton.addEventListener('click', function() {
                const suggestedTitle = suggestedTitleText.textContent.replace('제안된 제목: ', '');
                titleInput.value = suggestedTitle;
                suggestedTitleDiv.style.display = 'none';
            });
        } else {
            console.warn('One or more elements for title suggestion not found');
        }
    }

    function fetchSuggestedTitle(title) {
        fetch('/autocomplete-title/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({title: title})
        })
        .then(response => response.json())
        .then(data => {
            if (data.suggested_title && data.suggested_title !== title) {
                document.getElementById('suggested-title-text').textContent = `제안된 제목: ${data.suggested_title}`;
                document.getElementById('suggested-title').style.display = 'block';
            } else {
                document.getElementById('suggested-title').style.display = 'none';
            }
        })
        .catch(error => console.error('Error:', error));
    }

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
});