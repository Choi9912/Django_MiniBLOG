
    const roomName = JSON.parse(document.getElementById('room-name').textContent);
    const username = JSON.parse(document.getElementById('username').textContent);

    const chatSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/chat/' + roomName + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'chat_message') {
            addMessage(data.message);
        } else if (data.type === 'messages_read') {
            // Handle messages read event if needed
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };

    function addMessage(message) {
        const chatMessages = document.querySelector('#chat-messages');
        const messageElement = document.createElement('div');
        messageElement.className = `mb-2 ${message.sender === username ? 'text-right' : ''}`;
        messageElement.innerHTML = `
            <span class="px-2 py-1 rounded ${message.sender === username ? 'bg-blue-500 text-white' : 'bg-gray-200'}">
                ${message.content}
            </span>
            <div class="text-xs text-gray-500 mt-1">${new Date(message.timestamp).toLocaleString()}</div>
        `;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }