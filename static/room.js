const chatLog = document.querySelector('#chat-log')
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const gm = JSON.parse(document.getElementById('gm').textContent);
const user = JSON.parse(document.getElementById('user').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

function active(element_id) {
    chatSocket.send(JSON.stringify({
        'type': "token_active",
        'message': user + " " + element_id,
    }));
}

function can_active(element_id) {
    var divs = document.querySelectorAll(".element");
    divs.forEach((div) => {
        if (div.style.borderColor == "red") {
            div.style.borderColor = null;   
        }
    })
    
    var element;
    if (typeof element_id == 'string') {
        element = document.getElementById(element_id);
    }
    else element = element_id;   

    element.style.borderColor = "red";

    if (element.style.backgroundColor === "") {
        element.style.backgroundColor = "#ffffff";
    }

    active_element(element);
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    
    if (data.type == "add_grid_to_list") {
        if (document.getElementById('select_grid') != null) {
            var select_grid_var = document.getElementById('select_grid');
            var new_grid = document.createElement("button");
            new_grid.className = "btn btn-create-char";
            new_grid.id = data.id;
            new_grid.setAttribute("onclick", "activate_grid('" + new_grid.id + "')");
            new_grid.innerHTML = data.name + " (" + data.x + "x" + data.y + ")";
            select_grid_var.appendChild(new_grid);
        
            select_grid();
        }
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

        for (var i = 0; i < gridAreaWithCharacter.length; i += 4){
            var id = 'x' + gridAreaWithCharacter[i] + 'y' + gridAreaWithCharacter[i + 1];
            grid_area = document.getElementById(id);
            if (grid_area != null) {
                grid_area.innerHTML = gridAreaWithCharacter[i + 2];
                grid_area.style.backgroundColor = gridAreaWithCharacter[i + 3];

                set_text_color(gridAreaWithCharacter[i + 3], grid_area);
            }
        }
    }
    else if (data.type == "update_token") {
        var element_id = "x" + data.x + "y" + data.y;
        var element = document.getElementById(element_id);

        element.innerHTML = data.character;
        element.style.backgroundColor = data.color;

        set_text_color(data.color, element);
    }
    else if (data.type == "move_token") {
        var old_element = document.getElementById("x" + data.old_x + "y" + data.old_y);
        old_element.innerHTML = ""; old_element.style.background = null; old_element.style.borderColor = null; old_element.style.borderColor = null;

        var active_user = user.split(" ");

        if (document.getElementById("x" + data.new_x + "y" + data.new_y) != null) {
            var new_element = document.getElementById("x" + data.new_x + "y" + data.new_y);
            new_element.innerHTML = data.character; new_element.style.background = data.color;
            set_text_color(data.color, new_element);
            if (active_user[0] == data.user) {
                new_element.style.borderColor = "red";
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
    else if (data.type == "active_token") {
        var active_user = user.split(" ");

        if (active_user[0] == data.user) {
            var element = document.getElementById("x" + data.x + "y" + data.y);

            if (element.style.borderColor == "red") {
                element.style.borderColor = null;
                create_chat();
            }
            else {
                can_active(element.id);
            }
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
    console.error('Chat socket closed unexpectedly, press f5!');
};

function roll(message) {
    if (message.charAt(0) === '/') {
        message = message.replace("\n", '');

        let command = message.split(' ');
        let op = 1;
        let final_message = "";
        let roll_value;
        let roll_sum = 0;
        
        for (let i = 1; i < command.length; i++) {
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
                let roll_arr = [];
                for (let j = 0; j < times; j++) {
                    let curr_roll = Math.floor((Math.random() * sides) + 1);
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
        else if (isNaN(parseInt(command[2])) || isNaN(parseInt(command[3]))) {
            return ["error", "There was an error with your formula!"]
        }
        else if (parseInt(command[2]) > 50 || parseInt(command[3]) > 50) {
            return ["error", "Max grid size (50x50)!"]
        }
        message = command[1] + " " + parseInt(command[2]) + " " + parseInt(command[3]);
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

    var divs = document.querySelectorAll(".element");
    var active_id = "";
    divs.forEach((div) => {
        if (div.style.borderColor == "red") {
            active_id = div.id;
        }
    })

    if (input.value.length < 5) {
        var invalid_characters = " ,[]" + '"'
        var valid_name = true;

        for (var i = 0; i < input.value.length; i++){
            for (var j = 0; j < invalid_characters.length; j++){
                if (input.value[i] == invalid_characters[j]) {
                    valid_name = false;
                    alert("Invalid characters in token name!");
                }
            }
        }

        if (valid_name == true && active_id!="") {
            var message = active_id + " " + input.value;
            chatSocket.send(JSON.stringify({
                'type': "set_token_name",
                'message': message,
            }));
        }
        else if (active_id==""){
            console.log("Good try!");
        }
    }
    else{
        alert("4 letters maximum!");
    }
}

document.querySelector('#change_token_color').onchange = function (e) {
    var input = document.querySelector('#change_token_color');

    var divs = document.querySelectorAll(".element");
    var active_id = "";
    divs.forEach((div) => {
        if (div.style.borderColor == "red") {
            active_id = div.id;
        }
    })

    if (active_id != "") {
        var message = active_id + " " + input.value;

        chatSocket.send(JSON.stringify({
            'type': "set_token_color",
            'message': message
        }));
    }
    else {
        console.log("Good try!");
    }
}

function activate_grid(id) {
    chatSocket.send(JSON.stringify({
        'type': "activate_grid",
        'message': id,
    }))
}

function set_text_color(hex, element) {
    var count = 0;
    var light_color = "89abcdef";
    for (var j = 1; j < 6; j += 2){
        for (var z = 0; z < light_color.length; z++){
            if (hex[j] == light_color[z]) {
                count += 1;
            }
        }
    }

    if (count > 0) {
        element.style.color = "black";
    }
    else {
        element.style.color = "white";
    }
}

function websocket_send_token_move(key, id) {
    chatSocket.send(JSON.stringify({
        'type': "token_move",
        'message': key + " " + id,
    }));
}

let isKeyDown = false;
let keyDown = "";
let keyup_timeout;

document.addEventListener('keydown', (e) => {
    var divs = document.querySelectorAll(".element");

    var rows = document.querySelectorAll(".row").length;
    var columns = divs.length / rows;

    if (!isKeyDown) {
        divs.forEach((div) => {
            if (div.style.borderColor == "red" && div.innerHTML) {
                var id = div.id;
                var div_id = div.id.replace("x", "").split("y");
                if (e.keyCode == 38) {//up
                    if (div_id[1] != "0") {
                        var up_element = document.getElementById("x" + div_id[0] + "y" + (parseInt(div_id[1]) - 1).toString());
                        if (!up_element.innerHTML) {
                            websocket_send_token_move(id, "up");
                        }
                    }
                    else {
                        websocket_send_token_move(id, "up");
                    }

                    clearTimeout(keyup_timeout);

                    keyup_timeout = setTimeout(() => {
                        isKeyDown = false;
                    }, 300)

                    isKeyDown = true;
                }
                else if (e.keyCode == 40) {//down
                    if (div_id[1] != (rows-1).toString()) {
                        var down_element = document.getElementById("x" + div_id[0] + "y" + (parseInt(div_id[1]) + 1).toString());
                        if (!down_element.innerHTML) {
                            websocket_send_token_move(id, "down");
                        }
                    }
                    else {
                        websocket_send_token_move(id, "down");
                    }

                    clearTimeout(keyup_timeout);

                    keyup_timeout = setTimeout(() => {
                        isKeyDown = false;
                    }, 300)

                    isKeyDown = true;
                }
                else if (e.keyCode == 37) {//left
                    if (div_id[0] != "0") {
                        var left_element = document.getElementById("x" + (parseInt(div_id[0]) - 1).toString() + "y" + div_id[1]);
                        if (!left_element.innerHTML) {
                            websocket_send_token_move(id, "left");
                        }
                    }
                    else {
                        websocket_send_token_move(id, "left");
                    }
                
                    clearTimeout(keyup_timeout);

                    keyup_timeout = setTimeout(() => {
                        isKeyDown = false;
                    }, 300)

                    isKeyDown = true;
                }
                else if (e.keyCode == 39) {//right
                    if (div_id[0] != (columns-1).toString()) {
                        var right_element = document.getElementById("x" + (parseInt(div_id[0]) + 1).toString() + "y" + div_id[1]);
                        if (!right_element.innerHTML) {
                            websocket_send_token_move(id, "right");
                        }
                    }
                    else {
                        websocket_send_token_move(id, "right");
                    }

                    clearTimeout(keyup_timeout);

                    keyup_timeout = setTimeout(() => {
                        isKeyDown = false;
                    }, 300)

                    isKeyDown = true;
                }
            }
        })
    }
})