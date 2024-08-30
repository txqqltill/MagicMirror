Module.register("MMM-Face-Recognition-SMAI", {


defaults: {
  prompt: "",
  width: "200px",
  position: "left",
  refreshInterval: 2,
  id: "Guest"
},

start: function () {
  this.count = 0
},

getStyles: function () {
        return [
            this.file('css/mmm-style.css')
        ];
    },


getDom: function() {
    var element = document.createElement("div")
    element.className = "face-image"
    element.innerHTML = this.config.prompt
    element.id = this.config.id
    element.setAttribute("prompt", this.config.prompt)
    return element
},

//Create Socket Connnection with nodehelper.js
notificationReceived: function(notification, payload, sender) {
  switch(notification) {
    case "DOM_OBJECTS_CREATED":
      var timer = setInterval(()=>{
        this.sendSocketNotification("DO_YOUR_JOB", this.count)
        this.count++
      }, 1000)
      break
  }
},

login_user: function (currentUser) {

    var self = this;
    var defaultClass = "default"
    var everyoneClass = "everyone"
    
    MM.getModules().withClass(defaultClass).enumerate(function(module) {
	    module.hide(0, function() {
	    }, {lockString: self.identifier});
    });
    MM.getModules().withClass(currentUser).enumerate(function(module) {
	    module.show(0, function() {
	    }, {lockString: self.identifier});
    });
    MM.getModules().withClass(everyoneClass).enumerate(function(module) {
	    module.show(0, function() {
	    }, {lockString: self.identifier});
    });
},

//Recieve notification from socket of Python Variables via nodehelper.js
socketNotificationReceived: function(notification, payload) {
    this.login_user(payload);
    var elem = document.getElementById(payload)
    if(elem.getAttribute("prompt") === ""){
	elem.innerHTML = "Willkommen zurück, " + payload + "!";
    }else{
	elem.innerHTML = elem.getAttribute("prompt");
    }
    elem.classList.add(this.config.position);
    elem.style.width = this.config.width;
    var inner_div = document.createElement("div");
    var img = document.createElement("img");
    switch(notification) {
	case "I_DID":
	    img.setAttribute('src', "modules/MMM-Face-Recognition-SMAI/public/"+ payload +"-id.jpg");
	    break;
	default:
	    img.setAttribute('src', "modules/MMM-Face-Recognition-SMAI/public/guest.gif");
	    break;
    }
    inner_div.appendChild(img);
    elem.appendChild(inner_div)
    return elem
},
})
