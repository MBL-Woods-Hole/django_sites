function addEvent(to, type, fn){
    if(document.addEventListener){
        to.addEventListener(type, fn, false);
    } else if(document.attachEvent){
        to.attachEvent('on'+type, fn);
    } else {
        to['on'+type] = fn;
    }  
}

addEvent(window, 'load', show_alert);
function show_alert()
{
    // show_alert.onclick = alert("I am an alert box!");
    var row = document.getElementById('path_ext_msg').parentNode.parentNode;
    var msg   = "Please add a correct subdirectory name if needed!";
    var x = row.insertCell(2);
    x.innerHTML = msg;
    x.style.color = "red";
    // alert(msg);
}

