const currentUser = "{{ request.user.username }}";

const conversationSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/conversations/'
);

conversationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type === 'unread_count_update') {
        updateUnreadCount(data.conversation_id, data.unread_count);
    }
};

function updateUnreadCount(conversationId, unreadCount) {
    const conversationElement = document.querySelector(`[data-room-id="${conversationId}"]`);
    if (conversationElement) {
        let unreadBadge = conversationElement.querySelector('.unread-badge');
        if (unreadCount > 0) {
            if (unreadBadge) {
                unreadBadge.textContent = unreadCount;
            } else {
                unreadBadge = document.createElement('div');
                unreadBadge.className = 'bg-red-500 text-white rounded-full px-2 py-1 text-xs mt-1 unread-badge';
                unreadBadge.setAttribute('data-room-id', conversationId);
                unreadBadge.textContent = unreadCount;
                conversationElement.querySelector('.flex-col').appendChild(unreadBadge);
            }
        } else if (unreadBadge) {
            unreadBadge.remove();
        }
    }
}
