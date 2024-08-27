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