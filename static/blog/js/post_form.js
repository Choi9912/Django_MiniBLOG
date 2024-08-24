document.addEventListener('DOMContentLoaded', function() {
  // Select2 initialization for tags
  $('#{{ form.tags.id_for_label }}').select2({
      tags: true,
      tokenSeparators: [',', ' '],
      placeholder: "Enter tags",
  });
});


document.addEventListener('DOMContentLoaded', function() {
  const autocompleteUrl = '{% url "jeju_autocomplete" %}';

  CKEDITOR.plugins.add('autocomplete', {
    init: function(editor) {
      let typingTimer;
      const doneTypingInterval = 1000; // 1초 후에 자동완성 시작

      editor.on('key', function() {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(function() {
          const selection = editor.getSelection();
          const range = selection.getRanges()[0];
          const fragment = range.extractContents();
          const text = fragment.getFirst().getText();

          // 최소 2글자 이상 입력되었을 때만 자동완성 실행
          if (text.length >= 2) {
            fetch(`${autocompleteUrl}?query=${encodeURIComponent(text)}`)
              .then(response => response.json())
              .then(suggestions => {
                if (suggestions && suggestions.length > 0) {
                  showSuggestions(editor, suggestions);
                }
              })
              .catch(error => {
                console.error('Error:', error);
                editor.showNotification('자동완성 로드 중 오류가 발생했습니다.', 'warning');
              });
          }
        }, doneTypingInterval);
      });

      function showSuggestions(editor, suggestions) {
        const editorRect = editor.ui.contentsElement.getBoundingClientRect();
        const div = document.createElement('div');
        div.className = 'cke_autocomplete_panel';
        div.style.position = 'absolute';
        div.style.zIndex = '10000';
        div.style.left = `${editorRect.left}px`;
        div.style.top = `${editorRect.bottom + 5}px`;

        suggestions.forEach(suggestion => {
          const p = document.createElement('p');
          p.textContent = suggestion;
          p.onclick = function() {
            editor.insertText(` ${suggestion} `);
            document.body.removeChild(div);
          };
          div.appendChild(p);
        });

        // 이전에 생성된 제안 패널이 있다면 제거
        const oldPanel = document.querySelector('.cke_autocomplete_panel');
        if (oldPanel) {
          oldPanel.remove();
        }

        document.body.appendChild(div);
      }
    }
  });

  // CKEditor 설정에 개선된 자동완성 플러그인 추가
  CKEDITOR.replace('{{ form.content.auto_id }}', {
    extraPlugins: 'autocomplete',
    // 기타 CKEditor 설정...
  });
});
