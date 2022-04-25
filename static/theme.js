function switchFile(){
    var t = document.getElementById('themefile');
    if (t.getAttribute("href") == "/static/theme-light.css") {
        var th = 'dark';
        t.setAttribute("href", "/static/theme-dark.css");
    }
    else{
        t.setAttribute("href", "/static/theme-light.css");
        var th = 'light';
    }
}

