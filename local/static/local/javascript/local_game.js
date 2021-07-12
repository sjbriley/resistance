const game_ID = JSON.parse(document.getElementById('gameID').textContent);
const username = JSON.parse(document.getElementById('username').textContent);
const settings = JSON.parse(document.getElementById('settings').textContent) || '';
let userRoles = '';
let host = false;
const players = [username]
let updateSocket;

function connectSocket() {

    if (window.location.protocol == 'https:') {
        wsProtocol = 'wss://'
      } else {wsProtocol = 'ws://'}

    updateSocket = new WebSocket(
        wsProtocol + window.location.host + 
        '/local/wss/' + game_ID + '/');

    updateSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log("Received data:", e.data);
        if (data.username != username){
            if (data['init'] == true && host == true){
                updateSocket.send(JSON.stringify({
                    'gameID': game_ID,
                    'username': username,
                    'init': false,
                    'settings': settings,
                    'host': host,
                    'userRoles': userRoles,
                    }));
            }};
        if (data['init'] == true){
            document.getElementById('listUsers').innerHTML += ('<li class="list-group-item" stlye="font-size:1rem;">'+username+'</li>');
        };
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
            'username': username,
            'init': true,
            'settings': settings,
            'host': host,
            'userRoles': userRoles,
        }));
        updateWaitingPage()
    };
}

connectSocket();

window.onload = function() {
    document.getElementById('startGameClicked').onclick = function start_game_button(){
        console.log("Game started");
    }
};

function updateWaitingPage() {
    if (host) {
        button = document.getElementById("hostStartButton")
        button.style.display = 'block';
    }
    else {
        button = document.getElementById("guestWaitScreen")
        button.style.display = 'block';
    }
}

