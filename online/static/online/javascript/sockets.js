const game_ID = JSON.parse(document.getElementById('gameID').textContent);
const username = JSON.parse(document.getElementById('username').textContent);
const settings = JSON.parse(document.getElementById('settings').textContent) || '';
let host = false;
let init = false;
let updateSocket;

function connectSocket() {

    updateSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/sheet/' + game_ID + '/');

    updateSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log("Received data:", e.data);
    if (data.username != username){
        if (data['init'] == true && host == true){
            updateSocket.send(JSON.stringify({
                'gameID': game_ID,
                'message': '',
                'username': username,
                'init': init,
                'settings': settings,
                'host': host,
                }));
        }
    }
    };

    updateSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly; reconnecting');
    setTimeout(connectSocket, 1000);
    };

    updateSocket.onopen = function(e) {
    console.log("Socket connected; sending a ping");
    if (settings != ''){
        host = true;
    }
    console.log("Host joined, sending data");
    updateSocket.send(JSON.stringify({
    'gameID': game_ID,
    'message': '',
    'username': username,
    'init': true,
    'settings': settings,
    'host': host,
    }));
    };
}

function buttonClicked() {
    const textContent2 = document.getElementById("aaaaaa").value
    updateSocket.send(JSON.stringify({
    'gameID': game_ID,
    'message': textContent2,
    'username': username,
    'init': init,
    'settings': settings,
    'host': host,
    }));
};

connectSocket();