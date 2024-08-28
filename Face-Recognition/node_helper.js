var util = require("util");

var loggedIn = ""
/// node_helper.js
var NodeHelper = require("node_helper")

module.exports = NodeHelper.create({
  start: function() {
    this.countDown = 10000000
  },
  socketNotificationReceived: function(notification, payload) {
    switch(notification) {
      case "DO_YOUR_JOB":

  
      var fs = require('fs');
      fs.readFile("/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/sample.txt", function(err,data)
            {
                if(err)
                    console.log(err)
                else
                    face_rec_name = data.toString().replace(/\s+/g, '')
                   
                    console.log(face_rec_name);
            });
  
      fs.readdir('/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/public/', (err, datadir) => {
      
          if (err) throw err;
          if(face_rec_name.localeCompare("Guest") == 0)
          {
              //this.sendSocketNotification("I_NOT", loggedIn)
          }else
          {
                //this.sendSocketNotification("I_DID", loggedIn)
          }
      });
      fs.readdir('/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/public/', (err, datadir) => {
      
        
          if (err) throw err;
          if(face_rec_name.localeCompare("Guest") == 0)
          {
              //this.sendSocketNotification("I_NOT", loggedIn)
          }
        //if (face_rec_name.localeCompare(loggedIn) == 1){
        //  this.sendSocketNotification("I_DID", loggedIn)
        //}
        loggedIn = face_rec_name;
      });
     
      break
    }
  },
})
