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

var Biomes = [
  {
    key: 1,
    name: "marine",
    secondary_biome: ["pelagic", "bathyal", "hadal", "neritic", "abyssal", "continental margin"]
  }, {
    key: 2,
    name: "terrestrial",
    secondary_biome: ["aquatic", "freshwater lake", "freshwater river"]
  }, {
    key: 3,
    name: "subterrestrial",
    secondary_biome: ["aquatic"]
  }, {
    key: 4,
    name: "subseafloor",
    secondary_biome: ["aquatic", "continental margin"]
  }
];


//populate Biomes
// addEvent(window, 'load', populate_biomes);

function populate_biomes() {
  // alert("msg");
  
  biomes_menu = document.getElementById("Biomes");
  populateprimary_biome()
  //Populate initial secondary_biome
  populatesecondary_biome();
  
  biomes_menu.onchange = populatesecondary_biome()
}

function populateprimary_biome() {

for (var i = 0; i < Biomes.length; i++) {
  var opt = Biomes[i];
  var el = document.createElement("option");
  el.textContent = opt.name;
  el.value = opt.key;
  BiomesList.appendChild(el);
}
}

//populate secondary_biome
function populatesecondary_biome() {
  //clear the secondary_biome list
  document.getElementById('secondary_biomeList').options.length = 0;
  var e = document.getElementById("BiomesList");
  var selectedState = e.options[e.selectedIndex].value;
  var listOfsecondary_biome;
  for (var i = 0; i < Biomes.length; i++) {
    if (Biomes[i].key == selectedState) {
      listOfsecondary_biome = Biomes[i].secondary_biome;
      break;
    }
  }
  
  //populate secondary_biome DropDown menu
  for (var i = 0; i < listOfsecondary_biome.length; i++) {
    var opt = listOfsecondary_biome[i];
    var el = document.createElement("option");
    el.textContent = opt;
    el.value = opt;
    secondary_biomeList.appendChild(el);
  }
}
