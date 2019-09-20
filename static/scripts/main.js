window.onload = function() {
  faces();
}

var container = document.querySelector(".container");

function faces() {
  setInterval(getFaces, 5000);
}

function getFaces() {
  container.innerHTML = "";
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'get_faces', true);
  xhr.onload = function() {
    if(xhr.status == 200) {
      var names = JSON.parse(xhr.responseText);
      names.founds.forEach(function(name) {
        createCard(name);
      });
    }
  }
  xhr.send();
}

function createCard(name) {
  var pic = createPicture(name);
  var text = createText(name);
  var div = createDiv(pic, text);
  container.appendChild(div);
}

function createPicture(name) {
  var pic = document.createElement("picture");
  pic.classList.add("pic");
  var img = document.createElement("img");
  var src = "/static/known_people/" + name + ".jpg";
  img.src = src;
  img.alt = "foto";
  pic.appendChild(img);
  return pic;
}

function createText(name) {
  var p = document.createElement("p");
  p.classList.add("name");
  p.textContent = name;
  return p;
}

function createDiv(pic, text) {
  var div = document.createElement("div");
  div.classList.add("card");
  div.appendChild(pic);
  div.appendChild(text);
  return div;
}
