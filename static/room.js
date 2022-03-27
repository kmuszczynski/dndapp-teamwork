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
    messageUser.innerText = " "+data.messageAuthor+": "
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
        updateScroll();
    }

    if (document.querySelector('#emptyText')) {
        document.querySelector('#emptyText').remove()
    }
};
function updateScroll(){
    var scrolledDiv = document.getElementById("chat-log");
    scrolledDiv.scrollTop = scrolledDiv.scrollHeight;
}

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

function run_commands(message) {
    var command = message.split(' ');
    if (command[0] = '/roll' && message.charAt(0)=='/' && command[1].includes('d')) {
        var dice = command[1].split('d');
        if (dice.length != 2 || (dice[0] == "" || dice[1] == "") || (isNaN(dice[0]) || isNaN(dice[1])) || (dice[0].charAt(0) == "-" || dice[0].charAt(0) == "0")) return message;
        
        var n = parseInt(dice[0], 10);
        var d = parseInt(dice[1], 10);
        var arr = [];
        var sum = 0;

        for (var i = 0; i < n; i++){
            var v = Math.floor((Math.random() * d) + 1);
            sum = sum + v;
            arr.push(v);
        }

        return `Rolling ${n}d${d}: [${arr}] SUM: ${sum}`;
    }
    return message;
}

function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    if (!(isBlank(messageInputDom.value))) {
        var message = run_commands(messageInputDom.value);
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    }
};