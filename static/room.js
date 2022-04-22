const chatLog = document.querySelector('#chat-log')
const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

function active(element_id) {
    var divs = document.querySelectorAll(".element");
    divs.forEach((div) => {
        div.style.backgroundColor = "white";
    })
    
    var element;
    if (typeof element_id == 'string') {
        element = document.getElementById(element_id);
    }
    else element = element_id;   

    element.style.backgroundColor = "green";
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type == "grid") {
        var x = parseInt(data.x, 10);
        var y = parseInt(data.y, 10);
        var board = document.getElementById('board');
        board.innerHTML = "";
        for (var i = 0; i < y; i++) {
            var row = document.createElement('div'); row.className = "row"; row.id = i+1;
            for (var j = 0; j < x; j++){
                var element = document.createElement('div'); element.className = "element";
                var str = 'x' + (j + 1) + 'y' + (i + 1);
                element.id = str;
                element.setAttribute("onclick", 'active(' + str + ')');
                row.appendChild(element);
            }
            board.appendChild(row);
        }
    }
    else if (data.type == "message") {
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

function roll(message) {
    var command = message.split(' ');
    if (message.charAt(0)=='/' && command[1].includes('d')) {
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

function run_commands(message) {
    var command = message.split(' ');
    if (command[0] == '/roll') {
        message = roll(message);
        return ["roll", message]
    }
    if (command[0] == '/grid') {
        //dodac sprawdzanie poprawnosci liczb
        message = command[1] + " " + command[2];
        return ["grid", message]
    }
    else
        return ["message", message]
}

function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    if (!(isBlank(messageInputDom.value))) {
        var message = run_commands(messageInputDom.value);
        chatSocket.send(JSON.stringify({
            'type': message[0],
            'message': message[1]
        }));
        messageInputDom.value = '';
    }
};