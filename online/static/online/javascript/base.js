initial = true;
function toggleDropdown() {
    var x = document.getElementById("rolesPopup");
    if (x.style.display === "none" || initial == true) {
      x.style.display = "block";
      // initial is needed- for some reason on the first click it does not 
      // register as "none" so it takes 2 clicks to get here if not for initial check
      initial = false;
    } else {
      x.style.display = "none";
    }
  }

var mouse_over_main_card = false;
function show_main_card(card) {
  // document.getElementById("localCard").style.left = "40%";
  // document.getElementById("hoverShowLocal").style.left = "20%";
  document.getElementById("mainCard").style.zIndex = "100";

  document.getElementById("hoverShowAccount").innerHTML = "";
  document.getElementById("hoverShowLeaderboards").innerHTML = "";
  document.getElementById("hoverShowLocal").innerHTML = "";
  document.getElementById("hoverShowOnline").innerHTML = "";

  document.getElementById("hoverShowLocal").style.left = "14%";
  document.getElementById("hoverShowOnline").style.left = "14%";
  document.getElementById("hoverShowLocal").style.width = "9%";
  document.getElementById("hoverShowOnline").style.width = "9%";

  switch(card){
    case 'leaderboards':
      document.getElementById("hoverShowAccount").style.zIndex = "-20";
      document.getElementById("hoverShowOnline").style.zIndex = "-20";
      document.getElementById("hoverShowLocal").style.zIndex = "-20";
      document.getElementById("leaderboardsCard").style.display = "inline-block";
      break;
    case 'online':
      document.getElementById("hoverShowAccount").style.zIndex = "-20";
      document.getElementById("hoverShowLeaderboards").style.zIndex = "-20";
      document.getElementById("hoverShowLocal").style.zIndex = "-20";
      document.getElementById("onlineCard").style.display = "inline-block";
      break;
    case 'local':
      document.getElementById("hoverShowAccount").style.zIndex = "-20";
      document.getElementById("hoverShowLeaderboards").style.zIndex = "-20";
      document.getElementById("hoverShowOnline").style.zIndex = "-20";
      document.getElementById("localCard").style.display = "inline-block";
      
      break;
    case 'account':
      document.getElementById("hoverShowLeaderboards").style.zIndex = "-20";
      document.getElementById("hoverShowLocal").style.zIndex = "-20";
      document.getElementById("hoverShowOnline").style.zIndex = "-20";
      document.getElementById("accountCard").style.display = "inline-block";
      break;
    default:
      break;
    }

  document.getElementById("hoverShowAccount").style.left = "77%";
  document.getElementById("hoverShowLeaderboards").style.left = "77%";
  document.getElementById("hoverShowAccount").style.width = "9%";
  document.getElementById("hoverShowLeaderboards").style.width = "9%";
}

function hide_main_card() {
  setTimeout(function() {
    if (mouse_over_main_card == false){
      document.getElementById("localCard").style.display = "none";
      document.getElementById("leaderboardsCard").style.display = "none";
      document.getElementById("onlineCard").style.display = "none";
      document.getElementById("accountCard").style.display = "none";

      document.getElementById("mainCard").style.zIndex = "-25";
      document.getElementById("hoverShowAccount").style.zIndex = "20";
      document.getElementById("hoverShowOnline").style.zIndex = "20";
      document.getElementById("hoverShowLocal").style.zIndex = "20";
      document.getElementById("hoverShowLeaderboards").style.zIndex = "20";
      
      document.getElementById("hoverShowLocal").style.left = "24%";
      document.getElementById("hoverShowOnline").style.left = "24%";
      document.getElementById("hoverShowLocal").style.width = "25%";
      document.getElementById("hoverShowOnline").style.width = "25%";

      document.getElementById("hoverShowAccount").style.left = "51%";
      document.getElementById("hoverShowLeaderboards").style.left = "51%";
      document.getElementById("hoverShowAccount").style.width = "25%";
      document.getElementById("hoverShowLeaderboards").style.width = "25%";

      setTimeout(function() {
      document.getElementById("hoverShowLocal").innerHTML = "Local";
      document.getElementById("hoverShowOnline").innerHTML = "Online";
      document.getElementById("hoverShowAccount").innerHTML = "My Account";
      document.getElementById("hoverShowLeaderboards").innerHTML = "Leaderboards";
        }, 200);
    }
  }, 65);
}

function mouse_in_main_card() {
  mouse_over_main_card = true;
}
function mouse_out_main_card() {
  mouse_over_main_card = false;
  hide_main_card();
}
