const chatLog = document.querySelector('#chat-log')
const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageContainer = document.createElement('div')
    messageContainer.className = 'messageContainer'

    const messageUser = document.createElement('p')
    messageUser.innerText = data.messageAuthor+":"
    messageUser.className = 'messageUser'

    const messageDate = document.createElement('p')
    messageDate.innerText = '['+data.messageDateSent+']'
    messageDate.className = 'messageDate'

    const messageContent = document.createElement('p')
    messageContent.innerText = data.message
    messageContent.className = 'messageContent'

    messageContainer.appendChild(messageDate)
    messageContainer.appendChild(messageUser)
    messageContainer.appendChild(messageContent)
    if (data.message != ""){
        chatLog.appendChild(messageContainer)
    }

    if (document.querySelector('#emptyText')) {
        document.querySelector('#emptyText').remove()
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