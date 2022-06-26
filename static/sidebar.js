var objDiv = document.getElementById("chat-log");
objDiv.scrollTop = objDiv.scrollHeight;

function rgb_to_hex(rgb) {
    rgb = rgb.split(",");
    rgb[0] = rgb[0].replace('rgb(', '');
    rgb[1] = rgb[1].replace(' ', '');
    rgb[2] = rgb[2].replace(' ', '');
    rgb[2] = rgb[2].replace(')', '');

    var hex = "#"

    for (var i = 0; i < 3; i++) {
        var value = parseInt(rgb[i]).toString(16)
        if (value.length == 1) {
            value = "0"+value;
        }
        hex += value;
    }

    return hex;
}

function create_chat() {
    document.getElementById("char_list").style.display = 'none';
    document.getElementById("player_panel").style.display = 'none';
    document.getElementById("active_element").style.display = 'none';
    document.getElementById("select_grid").style.display = 'none';   

    document.getElementById("chat").style.display = 'block';
}

function get_character_list() {
    document.getElementById("chat").style.display = 'none';
    document.getElementById("player_panel").style.display = 'none';
    document.getElementById("active_element").style.display = 'none';
    document.getElementById("select_grid").style.display = 'none';   


    document.getElementById("char_list").style.display = 'block';
}

function player_panel() {
    document.getElementById("char_list").style.display = 'none';
    document.getElementById("chat").style.display = 'none';
    document.getElementById("active_element").style.display = 'none';
    document.getElementById("select_grid").style.display = 'none';   

    document.getElementById("player_panel").style.display = 'block';
}

function active_element(element) {
    document.getElementById("char_list").style.display = 'none';
    document.getElementById("chat").style.display = 'none';
    document.getElementById("player_panel").style.display = 'none';
    document.getElementById("select_grid").style.display = 'none';   

    var active = document.getElementById("active_element");
    active.style.display = 'block';
    var inputElements = active.querySelectorAll("input");
    inputElements[0].className = element.id;
    inputElements[1].className = element.id;

    inputElements[1].value = rgb_to_hex(element.style.backgroundColor.toString());

    if (element.textContent != null)
        inputElements[0].value = element.textContent;   
    else
        inputElements[0].value = "";
}

function select_grid() {
    document.getElementById("char_list").style.display = 'none';
    document.getElementById("chat").style.display = 'none';
    document.getElementById("player_panel").style.display = 'none';
    document.getElementById("active_element").style.display = 'none';

    document.getElementById("select_grid").style.display = 'block';
}