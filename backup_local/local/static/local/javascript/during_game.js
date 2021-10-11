window.onload = function() {
    document.getElementById('endGame').onclick = function(){
        console.log('here');
        document.getElementById('duringGame').style.display = 'none';
        document.getElementById('endGame').style.display = 'none';
        document.getElementById('resistanceWins').style.display = 'block';
        document.getElementById('spiesWin').style.display = 'block';
        document.getElementById('goBack').style.display = 'block';
    };
};