
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
      makeDiv(text);
      // child.appendChild(content);
      // parent.appendChild(child);

      return false;
    }
}

function makeDiv(message){
    // vary size for fun
    var color = '#808080';
    if (message.toLowerCase().indexOf('swan') != -1 || message.toLowerCase().indexOf('syd') != -1) {
      color = '#cc0000'
    } else if (message.toLowerCase().indexOf('dog') != -1) {
      color = "#0033cc"
    }
    $newdiv = $('<div/>').css({
        'width':'350px',
        'background-color': color,
      'border': '1pt solid black',
      "border-radius": "25px",
      "padding": "10px"
    });

    // make position sensitive to size and document's width
    var posx = (Math.random() * ($(document).width() - 350)).toFixed();
    var posy = (Math.random() * ($(document).height() - 200)).toFixed();
    $newdiv.html(message);

    $newdiv.css({
        'position':'absolute',
        'left':posx+'px',
        'top':posy+'px',
        'display':'none'
    }).appendTo( 'body' ).fadeIn(500).delay(5000).fadeOut(1000, function(){
      $(this).remove();
    });
}

$(document).ready(function(){
console.log('I am ready');
listen();
});