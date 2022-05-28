const chatLog = document.querySelector('#chat-log')
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const gm = JSON.parse(document.getElementById('gm').textContent);

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
        if (div.style.backgroundColor == "green") {
            div.style.backgroundColor = "white";   
        }
    })
    
    var element;
    if (typeof element_id == 'string') {
        element = document.getElementById(element_id);
    }
    else element = element_id;   

    element.style.backgroundColor = "green";

    active_element(element);
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    
    if (data.type == "add_grid_to_list") {
        var select_grid_var = document.getElementById('select_grid');
        var new_grid = document.createElement("button");
        new_grid.className = "btn btn-create-char";
        new_grid.id = data.id;
        new_grid.setAttribute("onclick", "activate_grid('" + new_grid.id + "')");
        new_grid.innerHTML = data.name + " (" + data.x + "x" + data.y + ")";
        select_grid_var.appendChild(new_grid);
        
        select_grid();
    }
    else if (data.type == "change_grid") {
        var x = parseInt(data.x, 10);
        var y = parseInt(data.y, 10);
        var gridAreaWithCharacter = data.gridAreaWithCharacter.replaceAll(']', '').replaceAll('[', '').replaceAll(',', '').replaceAll('"', '').split(" ");

        var board = document.getElementById('board');
        board.innerHTML = "";
        for (var i = 0; i < y; i++) {
            var row = document.createElement('div'); row.className = "row"; row.id = i;
            for (var j = 0; j < x; j++){
                var element = document.createElement('div'); element.className = "element";
                element.id = 'x' + j + 'y' + i;
                element.setAttribute("onclick", 'active(' + element.id + ')');
                row.appendChild(element);
            }
            board.appendChild(row);
        }

        for (var i = 0; i < gridAreaWithCharacter.length; i += 3){
            var id = 'x' + gridAreaWithCharacter[i] + 'y' + gridAreaWithCharacter[i + 1];
            grid_area = document.getElementById(id);
            grid_area.innerHTML = gridAreaWithCharacter[i + 2];
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

function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}

function run_commands(message) {
    var command = message.split(' ');
    if (command[0] == '/roll') {
        message = roll(message);
        return ["roll", message]
    }
    if (command[0] == '/grid') {
        if (command.length != 4) {
            return ["error", "There was an error with your formula!"]
        }
        else if (gm != true) {
            return ["error", "You can't use this command!"]
        }
        //walidacja danych potrzebna!!!
        message = command[1] + " " + command[2] + " " + command[3];
        return ["grid", message]
    }
    else
        return ["message", message]
}

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    if (!(isBlank(messageInputDom.value))) {
        var message = run_commands(messageInputDom.value);
        if (message[0] != "error") {
            chatSocket.send(JSON.stringify({
                'type': message[0],
                'message': message[1]
             }));
            messageInputDom.value = '';
        }
        else {
            const messageContainer = document.createElement('div');
            messageContainer.className = 'messageContainer';

            const messageContent = document.createElement('p');
            messageContent.innerText = message[1];
            messageContent.className = 'messageContent';

            messageContainer.append(messageContent);
            chatLog.append(messageContainer)
        }
    }
};

document.querySelector('#token_name_input').focus();
document.querySelector('#token_name_input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#token_name_button').click();
    }
};

document.querySelector('#token_name_button').onclick = function (e) {
    var input = document.querySelector('#token_name_input');
    var element = document.getElementById(input.className);
    element.innerHTML = input.value;
}


function activate_grid(id) {
    chatSocket.send(JSON.stringify({
        'type': "activate_grid",
        'message': id,
    }))
}