var objDiv = document.getElementById("chat-log");
objDiv.scrollTop = objDiv.scrollHeight;

function create_chat() {
    document.getElementById("char_list").style.display = 'none';
    document.getElementById("player_panel").style.display = 'none';
    document.getElementById("active_element").style.display = 'none';

    document.getElementById("chat").style.display = 'block';
}

function get_character_list() {
    document.getElementById("chat").style.display = 'none';
    document.getElementById("player_panel").style.display = 'none';
    document.getElementById("active_element").style.display = 'none';

    document.getElementById("char_list").style.display = 'block';
}

function player_panel() {
    document.getElementById("char_list").style.display = 'none';
    document.getElementById("chat").style.display = 'none';
    document.getElementById("active_element").style.display = 'none';

    document.getElementById("player_panel").style.display = 'block';
}

function active_element(element) {
    document.getElementById("char_list").style.display = 'none';
    document.getElementById("chat").style.display = 'none';
    document.getElementById("player_panel").style.display = 'none';

    var active = document.getElementById("active_element");
    active.style.display = 'block';
    var inputElements = active.querySelectorAll("input");
    inputElements[0].className = element.id;
    if (element.textContent != null) inputElements[0].value = element.textContent;   
    else inputElements[0].value = "";
}