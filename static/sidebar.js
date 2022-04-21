var objDiv = document.getElementById("chat-log");
objDiv.scrollTop = objDiv.scrollHeight;

function create_chat() {
    document.getElementById("char_list").style.display = 'none';
    document.getElementById("player_panel").style.display = 'none';

    document.getElementById("chat").style.display = 'block';
}

function get_character_list() {
    document.getElementById("chat").style.display = 'none';
    document.getElementById("player_panel").style.display = 'none';

    document.getElementById("char_list").style.display = 'block';
}

function player_panel() {
    document.getElementById("char_list").style.display = 'none';
    document.getElementById("chat").style.display = 'none';

    document.getElementById("player_panel").style.display = 'block';
}