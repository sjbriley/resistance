const game_id = JSON.parse(document.getElementById('game_id').textContent);
const username = JSON.parse(document.getElementById('username').textContent);
const settings = JSON.parse(document.getElementById('settings').textContent) || '';
let user_roles = '';
let users = [username];
let listed_players = [];
let host = false;
let players = [username]
let updateSocket;
let myRole = []


function connectSocket() {

    // connect to the socket
    if (window.location.protocol == 'https:') {
        wsProtocol = 'wss://'
      } else {wsProtocol = 'ws://'}
    updateSocket = new WebSocket(
        wsProtocol + window.location.host + 
        '/local/wss/' + game_id + '/');

    // lose connection to websocket, try to reconnect
    updateSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly; reconnecting');
        setTimeout(connectSocket, 1000);
    };

    // what happens when you first connect to websocket
    updateSocket.onopen = function(e) {
        console.log("Socket connected; sending a ping");

        // if host joined with settings, send settings to LocalGames model
        if (settings != ''){
            host = true;
            console.log("Host joined, sending data");
            updateSocket.send(JSON.stringify({
                'init': true,
                'settings': settings,
                'host': host,
            }));
        };
        
        // Request a list of users when joining
        updateSocket.send(JSON.stringify({
            'username': username,
            'new_user_joined': true,       
        }));
        
        // update HTML with either 'start game' button or 'waiting for host'
        updateWaitingPage()
    };

    // process messages
    updateSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log("Received data:", e.data);

        // if you or any other user join for first time
        if (data['new_user_joined'] == true){
            players = data['players'];
            for (let i = 0; i < players.length; i++){
                if (listed_players.includes(players[i]) !== true) {
                    console.log('here')
                    listed_players.push(players[i]);
                    document.getElementById('listUsers').innerHTML += ('<li class="list-group-item" stlye="font-size:1rem;">'+players[i]+'</li>');
                }
            if (host){
                document.getElementById('errorStarting').style.display = 'none';
            }
            }
        };

        // if host hits 'start game', then process LocalGames response with roles and update HTML
        if (data['game_started'] == true) {
            // myRole = data['user_roles'][username]
            document.getElementById('startGameClicked').style.display = 'none';
            document.getElementById('guestWaitScreen').style.display = 'none';
            document.getElementById('listUsers').style.display = 'none';
            if (host) {
                document.getElementById('endGame').style.display = 'block';
            }
        };

        if (data['game_finished'] === true){
            document.getElementById('listUsers').style.display = 'none';
            document.getElementById('guestWaitScreen').style.display = 'none';
            document.getElementById('endGameButtons').style.display = 'none';
            if (!host) {
                if (data['winner'] === 'spies'){
                    showSpyWinner()
                }
                else {
                    showResistanceWinner()
                }
            }
        }
    };
}

connectSocket();

// connect 'start game' button with a funciton when clicked to send message on socket
window.onload = function() {
    document.getElementById('startGameClicked').onclick = function start_game_button(){
        console.log("Game started");
        if (players.length > 10 || players.length < 5){
            document.getElementById('errorStarting').innerHTML = "<span style='color:red;'>Not enough or too many players</span>";
        }
        else {
            updateSocket.send(JSON.stringify({
                'game_started': true,
            }));
        }
        // REMOVE THIS BELOW
        updateSocket.send(JSON.stringify({
            'game_started': true,
        }));
        document.getElementById('errorStarting').style.display = 'none';
    };

    document.getElementById('endGame').onclick = function(){
        document.getElementById('duringGame').style.display = 'none';
        document.getElementById('endGame').style.display = 'none';
        document.getElementById('endGameButtons').style.display = 'block';
    };

    document.getElementById('goBack').onclick = function(){
        document.getElementById('duringGame').style.display = 'block';
        document.getElementById('endGameButtons').style.display = 'none';
        if (host) {
            document.getElementById('endGame').style.display = 'block';
        };
    };

    document.getElementById('resistanceWins').onclick = function showResistanceWinner(){
        if (host){
            updateSocket.send(JSON.stringify({
                'game_finished': true,
                'winner': 'resistance',
            }));
        };
        document.getElementById('showWinner').innerHTML = "<br><br><span style='font-size:2rem;color:blue;'>Resistance Wins!</span>";
        document.getElementById('showWinner').style.display = 'block';
    };

    document.getElementById('spiesWin').onclick = function showSpyWinner(){
        // send websocket message updating others to call this function
        if (host){
            updateSocket.send(JSON.stringify({
                'game_finished': true,
                'winner': 'spies',
            }));
        };
        document.getElementById('showWinner').innerHTML = "<br><br><span style='font-size:2rem;color:red;'>Spies Win!</span>";
        document.getElementById('showWinner').style.display = 'block';
    };
};

// Update page with either 'start game' or 'waiting for host'
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

