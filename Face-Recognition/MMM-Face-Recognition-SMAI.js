Module.register("MMM-Face-Recognition-SMAI", {


defaults: {
  prompt: "Use FaceID to access profiles",
  width: "200px",
  position: "left",
  refreshInterval: 2
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
  var subElement = document.createElement("p")
  subElement.id = "COUNT"
  element.appendChild(subElement)

 
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
	    module.show(1000, function() {
	    }, {lockString: self.identifier});
    });
    MM.getModules().withClass(everyoneClass).enumerate(function(module) {
	    module.show(1000, function() {
	    }, {lockString: self.identifier});
    });
},

//Recieve notification from socket of Python Variables via nodehelper.js
socketNotificationReceived: function(notification, payload) {
    this.login_user(payload);
    var elem = document.getElementById("COUNT")
    elem.innerHTML = "Welcome back, " + payload
    elem.classList.add(this.config.position);
    elem.style.width = this.config.width;
    var img = document.createElement("img");
    switch(notification) {
	case "I_DID":
	    img.setAttribute('src', "modules/MMM-Face-Recognition-SMAI/public/"+ payload +"-id.jpg");
	    break;
	default:
	    img.setAttribute('src', "modules/MMM-Face-Recognition-SMAI/public/guest.gif");
	    break;
    }
    elem.appendChild(img);
    return elem
},
})
