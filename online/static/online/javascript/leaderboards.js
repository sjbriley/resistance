function ChangeDropdowns(value){
    var show;
    var text;
    var hide = [];
    if ( value == '1') {show = document.getElementsByClassName("resistanceWins"); text='Resistance Wins';}
    else {hide.push(document.getElementsByClassName("resistanceWins"));}
    
    if ( value == '2') {show = document.getElementsByClassName("spyWins"); text='Spy Wins';}
    else {hide.push(document.getElementsByClassName("spyWins"));}
    
    if ( value == '3') {show = document.getElementsByClassName("resistanceLosses"); text='Resistance Losses';}
    else {hide.push(document.getElementsByClassName("resistanceLosses"));}
    
    if ( value == '4') {show = document.getElementsByClassName("spyLosses"); text='Spy Losses';}
    else {hide.push(document.getElementsByClassName("spyLosses"));}
    
    if ( value == '5') {show = document.getElementsByClassName("jesterWins"); text='Jester Wins';}
    else {hide.push(document.getElementsByClassName("jesterWins"));}
    
    if ( value == '6') {show = document.getElementsByClassName("merlinWins"); text='Merlin Wins';}
    else {hide.push(document.getElementsByClassName("merlinWins"));}
    
    if ( value == '7') {show = document.getElementsByClassName("puckWins"); text='Puck Wins';}
    else {hide.push(document.getElementsByClassName("puckWins"));}
    
    if ( value == '8') {show = document.getElementsByClassName("lancelotWins"); text='Lancelot Wins';}
    else {hide.push(document.getElementsByClassName("lancelotWins"));}

    for (var i=0; i < show.length; i += 1){
        show[i].style.display = 'block';
    };
    document.getElementById("tableName").innerHTML = text 

    hide.forEach(function(item){
        for (var i=0; i < item.length; i += 1){
            item[i].style.display = 'none';
        };
    })
}

