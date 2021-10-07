const game_ID = JSON.parse(document.getElementById('game_id').textContent);
const username = JSON.parse(document.getElementById('username').textContent);
const settings = JSON.parse(document.getElementById('settings').textContent) || '';
let user_roles = '';
let host = false;
let init = false;
let updateSocket;

function connectSocket() {

    // not using https
    if (window.location.protocol == 'https:') {
        wsProtocol = 'ws://'
      } else {wsProtocol = 'ws://'}

    if (window.location.host.includes('8000')){
        updateSocket = new WebSocket(
            wsProtocol + window.location.host + 
            '/online/ws/' + game_ID + '/');
    }
    else{
        updateSocket = new WebSocket(
            wsProtocol + window.location.host + 
            ':8001/online/ws/' + game_ID + '/');
    }
    }

    updateSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log("Received data:", e.data);
    if (data.username != username){
        if (data['init'] == true && host == true){
            updateSocket.send(JSON.stringify({
                'game_id': game_ID,
                'gameType': 'online',
                'username': username,
                'init': init,
                'settings': settings,
                'host': host,
                'user_roles': user_roles,
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
        'game_id': game_ID,
        'gameType': 'online',
        'username': username,
        'init': true,
        'settings': settings,
        'host': host,
        'user_roles': user_roles,
        }));
    };
}

connectSocket();

// window.onload = function() {
//     document.getElementById("changeJester").onclick = function changeJester() {
//         console.log("clicked");
//         if (settings['jester'] == true) {
//             settings['jester'] = false;
//             updateSocket.send(JSON.stringify({
//                 'settings': settings,
//             }));
//         }
//         else {
//             settings['jester'] = true;
//             updateSocket.send(JSON.stringify({
//                 'settings': settings,
//             }));
//         }
//     };
// };