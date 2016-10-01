
//function that listens to Socket and do something when notification comes
function listen() {
    var source = new WebSocket('ws://' + window.location.host + '/ws');
    var parent = document.getElementById("container");
    source.onmessage = function(msg) {
      console.log('received');
      var message = JSON.parse(msg.data);
      var text = message['text'];
      var child = document.createElement("DIV");
      var content = document.createTextNode(text);
      child.appendChild(content);
      parent.appendChild(child);
      return false;
    }
}

$(document).ready(function(){
console.log('I am ready');
listen();
});