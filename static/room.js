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
            if(grid_area != null){
                grid_area.innerHTML = gridAreaWithCharacter[i + 2];
            }
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
    if (message.charAt(0) === '/') {
        message = message.replace(/\n$/, '');
        var command = message.split(' ');
        var op = 1;
        var final_message = "";
        var roll_value;
        var roll_sum = 0;
        
        for (var i = 1; i < command.length; i++) {
            if (command[i].includes('d')) {
                if (i !== 1) {
                    final_message += "\n";
                }

                dice_roll = command[i].split('d');

                if (dice_roll.length !== 2) {
                    return ["error", "Too many 'd's in your roll call!"];
                }

                if (dice_roll[0] === "0") {
                  return ["error", "You can't roll 0 times... Come on :/"];
                }

                if (!/^\d+$/.test(dice_roll[0]) && dice_roll[0] !== "") {
                  return ["error", "Write 1 or higher before d in roll call!"];
                }

                times = (dice_roll[0] === "") ? 1 : parseInt(dice_roll[0], 10);

                if (!/^\d+$/.test(dice_roll[1])) {
                    return ["error", "Write a numeric value after 'd' >:("];
                }

                sides = parseInt(dice_roll[1], 10);

                roll_value = 0;
                var roll_arr = [];
                for (var j = 0; j < times; j++) {
                    var curr_roll = Math.floor((Math.random() * sides) + 1);
                    roll_value += curr_roll;
                    roll_arr.push(curr_roll);
                }

                if (op !== 0) {
                    if (op === 1) {
                        roll_sum += roll_value;
                    } else {
                        roll_sum -= roll_value;
                    }
                    op = 0;
                }

                final_message += `Rolling ${times}d${sides}: [${roll_arr}] SUM: ${roll_value}`;
            } 
            else if (command[i] === '+') {
                op = 1;
            }
            else if (command[i] === '-') {
                op = -1;
            }
            else if (/^\d+$/.test(command[i])) {
                bonus = parseInt(command[i], 10);

                if (op !== 0) {
                    if (op === 1) {
                        final_message += `\nBonus +${bonus}`;
                        roll_sum += bonus;
                    } else {
                        final_message += `\nPenalty -${bonus}`;
                        roll_sum -= bonus;
                    }
                    op = 0;
                }
            }
            else {
                return ["error", "Invalid element of roll call!"];
            }
        }

        final_message += `\nSUM OF ROLLS: ${roll_sum}`;

        return ["roll", final_message];
    }
    return message;
}

function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}

function run_commands(message) {
    var command = message.split(' ');
    if (command[0] == '/roll') {
        return roll(message);
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

    var message = input.className + " " + input.value;
    chatSocket.send(JSON.stringify({
        'type': "set_token_name",
        'message': message,
    }));
}

function activate_grid(id) {
    chatSocket.send(JSON.stringify({
        'type': "activate_grid",
        'message': id,
    }))
}