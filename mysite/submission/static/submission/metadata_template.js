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

var States = [{
  key: 13,
  name: "State1",
  cities: ["City1", "City2", "Silver Spring"]
}, {
  key: 2,
  name: "State2",
  cities: ["City5", "City9", "City8","San Diego"]
}];
//populate states
for (var i = 0; i < States.length; i++) {
  var opt = States[i];
  var el = document.createElement("option");
  el.textContent = opt.name;
  el.value = opt.key;
  StatesList.appendChild(el);
}
//Populate initial cities
populateCities();


//populate cities
function populateCities() {
  //clear the cities list
  document.getElementById('CitiesList').options.length = 0;
  var e = document.getElementById("StatesList");
  var selectedState = e.options[e.selectedIndex].value;
  var listOfCities;
  for (var i = 0; i < States.length; i++) {
    if (States[i].key == selectedState) {
      listOfCities = States[i].cities;
      break;
    }
  }
  //populate Cities DropDown menu
  for (var i = 0; i < listOfCities.length; i++) {
    var opt = listOfCities[i];
    var el = document.createElement("option");
    el.textContent = opt;
    el.value = opt;
    CitiesList.appendChild(el);
  }
}
