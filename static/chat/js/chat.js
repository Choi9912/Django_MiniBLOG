document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatLog = document.getElementById('chat-log');
    const messageInput = document.getElementById('chat-message-input');

    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(chatForm);
        
        fetch("{% url 'chat:send_message' conversation.id %}", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'mb-4 text-right';
                messageDiv.innerHTML = `
                    <div class="inline-block bg-blue-500 text-white rounded-lg px-4 py-2 max-w-xs lg:max-w-md">
                        ${data.content}
                    </div>
                    <div class="text-xs text-gray-500 mt-1">
                        ${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </div>
                `;
                chatLog.appendChild(messageDiv);
                messageInput.value = '';
                chatLog.scrollTop = chatLog.scrollHeight;
            } else {
                console.error('Error sending message:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // 페이지 로드 시 스크롤을 아래로 내립니다.
    chatLog.scrollTop = chatLog.scrollHeight;
});