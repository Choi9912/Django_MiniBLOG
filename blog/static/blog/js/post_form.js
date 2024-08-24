document.addEventListener('DOMContentLoaded', function() {
  console.log('DOMContentLoaded event fired');
  if (typeof autocompleteUrl === 'undefined') {
    console.error('autocompleteUrl is not defined');
    return;
  } else {
      console.log('autocompleteUrl:', autocompleteUrl);
  }
  if (typeof tagsFieldId === 'undefined') {
      console.error('tagsFieldId is not defined');
      return;
  }
  if (typeof contentFieldId === 'undefined') {
      console.error('contentFieldId is not defined');
      return;
  }
  


  // Initialize Select2 for tags
  if ($('#' + tagsFieldId).length) {
      $('#' + tagsFieldId).select2({
          tags: true,
          tokenSeparators: [',', ' '],
          placeholder: "Enter tags",
      });
  } else {
      console.warn('Tags field not found');
  }

  // Initialize Summernote
  if ($('#' + contentFieldId).length) {
      $('#' + contentFieldId).summernote({
          height: 300,
          callbacks: {
              onInit: function() {
                  console.log('Summernote initialized');
                  $(this).summernote('code', ''); // Start with empty content
              },
              onChange: function(contents, $editable) {
                  console.log('Content changed:', contents);
              }
          }
      });

      // Listen for Ctrl+Alt key combination to trigger autocomplete
      $(document).on('keydown', function(e) {
          if (e.ctrlKey && e.altKey) {
              e.preventDefault();
              triggerAutocomplete();
          }
      });
  } else {
      console.warn('Content field not found');
  }

  function triggerAutocomplete() {
      console.log('Autocomplete triggered');
      const editorContent = $('#' + contentFieldId).summernote('code');
      const lastWord = editorContent.split(/\s+/).pop(); // Get the last word

      if (lastWord.length > 0) {
          $.ajax({
              url: autocompleteUrl,
              data: { q: lastWord },
              success: function(suggestions) {
                  console.log('Suggestions:', suggestions);
                  showSuggestions(suggestions);
              },
              error: function(xhr, status, error) {
                  console.error('Autocomplete error:', error);
              }
          });
      } else {
          console.warn('No valid input for autocomplete');
      }
  }

  function showSuggestions(suggestions) {
      const editor = $('#' + contentFieldId);
      const editorPos = editor.offset();
      const div = document.createElement('div');
      div.className = 'summernote_autocomplete_panel';
      div.style.position = 'absolute';
      div.style.zIndex = '10000';
      div.style.left = `${editorPos.left}px`;
      div.style.top = `${editorPos.top + editor.outerHeight()}px`;

      suggestions.forEach(suggestion => {
          const p = document.createElement('p');
          p.textContent = suggestion;
          p.onclick = function() {
              editor.summernote('insertText', ` ${suggestion} `);
              document.body.removeChild(div);
          };
          div.appendChild(p);
      });

      const oldPanel = document.querySelector('.summernote_autocomplete_panel');
      if (oldPanel) {
          oldPanel.remove();
      }

      document.body.appendChild(div);
  }
});
$(document).ready(function() {
    $('#suggest-title-btn').click(function() {
        var originalTitle = $('#id_title').val();
        if (originalTitle) {
            $.ajax({
                url: '/suggest-title/',  // URL을 하드코딩하지 않고 동적으로 가져오는 방법을 고려해보세요
                data: {'title': originalTitle},
                method: 'GET',
                beforeSend: function() {
                    $('#suggest-title-btn').prop('disabled', true).text('제안 중...');
                },
                success: function(data) {
                    if (data.suggested_title) {
                        $('#suggested-title').text('제안된 제목: ' + data.suggested_title)
                            .show();
                    }
                },
                error: function() {
                    alert('제목 제안 중 오류가 발생했습니다.');
                },
                complete: function() {
                    $('#suggest-title-btn').prop('disabled', false).text('제목 제안받기');
                }
            });
        } else {
            alert('제목을 먼저 입력해주세요.');
        }
    });
});