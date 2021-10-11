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

  document.getElementById("hoverShowAccount").innerHTML = "";
  document.getElementById("hoverShowLeaderboards").innerHTML = "";
  // document.getElementById("hoverShowLocal").innerHTML = "";
  document.getElementById("hoverShowOnline").innerHTML = "";

  document.getElementById("mainCard").style.zIndex = "100";

  document.getElementById("accountCard").style.display = "none";
  // document.getElementById("localCard").style.display = "none";
  document.getElementById("onlineCard").style.display = "none";
  document.getElementById("leaderboardsCard").style.display = "none";
  document.getElementById("hoverShowLeaderboards").style.zIndex = "-20";
  // document.getElementById("hoverShowLocal").style.zIndex = "-20";
  document.getElementById("hoverShowAccount").style.zIndex = "-20";
  document.getElementById("hoverShowOnline").style.zIndex = "-20";

  switch(card){
    case 'leaderboards':
      document.getElementById("hoverShowLeaderboards").style.zIndex = "20";
      document.getElementById("leaderboardsCard").style.display = "inline-block";
      document.getElementById("hoverShowLeaderboards").style.left = "77%";
      document.getElementById("hoverShowLeaderboards").style.width = "15%";
      break;
    case 'online':
      document.getElementById("hoverShowOnline").style.zIndex = "20";
      document.getElementById("onlineCard").style.display = "inline-block";
      break;
    // case 'local':
    //   document.getElementById("hoverShowLocal").style.zIndex = "20";
    //   document.getElementById("localCard").style.display = "inline-block";
      
      break;
    case 'account':
      document.getElementById("hoverShowAccount").style.zIndex = "20";
      document.getElementById("accountCard").style.display = "inline-block";
      break;
    default:
      break;
    }

  document.getElementById("hoverShowAccount").style.left = "77%";
  document.getElementById("hoverShowLeaderboards").style.left = "77%";
  document.getElementById("hoverShowAccount").style.width = "9%";
  document.getElementById("hoverShowLeaderboards").style.width = "9%";

  // document.getElementById("hoverShowLocal").style.left = "14%";
  document.getElementById("hoverShowOnline").style.left = "14%";
  // document.getElementById("hoverShowLocal").style.width = "9%";
  document.getElementById("hoverShowOnline").style.width = "9%";

  // does not always upadate at beggining for some reason- clear HTML twice
  setTimeout(function() {
    document.getElementById("hoverShowAccount").innerHTML = "";
    document.getElementById("hoverShowLeaderboards").innerHTML = "";
    // document.getElementById("hoverShowLocal").innerHTML = "";
    document.getElementById("hoverShowOnline").innerHTML = "";
      }, 400);
}

function hide_main_card() {
  setTimeout(function() {
    if (mouse_over_main_card == false){
      // document.getElementById("localCard").style.display = "none";
      document.getElementById("leaderboardsCard").style.display = "none";
      document.getElementById("onlineCard").style.display = "none";
      document.getElementById("accountCard").style.display = "none";

      document.getElementById("mainCard").style.zIndex = "-25";
      document.getElementById("hoverShowAccount").style.zIndex = "20";
      document.getElementById("hoverShowOnline").style.zIndex = "20";
      // document.getElementById("hoverShowLocal").style.zIndex = "20";
      document.getElementById("hoverShowLeaderboards").style.zIndex = "20";
      
      // document.getElementById("hoverShowLocal").style.left = "24%";
      document.getElementById("hoverShowOnline").style.left = "24%";
      // document.getElementById("hoverShowLocal").style.width = "25%";
      document.getElementById("hoverShowOnline").style.width = "25%";

      document.getElementById("hoverShowAccount").style.left = "51%";
      document.getElementById("hoverShowLeaderboards").style.left = "51%";
      document.getElementById("hoverShowAccount").style.width = "25%";
      document.getElementById("hoverShowLeaderboards").style.width = "25%";

      setTimeout(function() {
      // document.getElementById("hoverShowLocal").innerHTML = "Local";
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

// MOBILE BELOW ================================
function show_main_card_mobile(card) {

  document.getElementById("mainCard_mobile").style.zIndex = "100";

  document.getElementById("accountCard_mobile").style.display = "none";
  // document.getElementById("localCard_mobile").style.display = "none";
  document.getElementById("onlineCard_mobile").style.display = "none";
  document.getElementById("leaderboardsCard_mobile").style.display = "none";
  document.getElementById("hoverShowAccount_mobile").style.zIndex = "-20";
  document.getElementById("hoverShowOnline_mobile").style.zIndex = "-20";
  // document.getElementById("hoverShowLocal_mobile").style.zIndex = "-20";
  document.getElementById("hoverShowLeaderboards_mobile").style.zIndex = "-20";

  switch(card){
    case 'leaderboards':
      document.getElementById("hoverShowLeaderboards_mobile").style.zIndex = "20";
      document.getElementById("leaderboardsCard_mobile").style.display = "inline-block";
      document.getElementById("leaderboardsCard_mobile").style.top = "31%";
      document.getElementById("hoverShowLeaderboards_mobile").style.bottom = "80%";
      document.getElementById("hoverShowLeaderboards_mobile").style.zIndex = "-20";
      break;
    case 'online':
      document.getElementById("hoverShowOnline_mobile").style.zIndex = "20";
      document.getElementById("onlineCard_mobile").style.display = "inline-block";
      document.getElementById("onlineCard_mobile").style.top = "31%";
      document.getElementById("hoverShowOnline_mobile").style.bottom = "80%";
      document.getElementById("hoverShowOnline_mobile").style.zIndex = "-20";
      break;
    // case 'local':
    //   document.getElementById("hoverShowLocal_mobile").style.zIndex = "20";
    //   document.getElementById("localCard_mobile").style.display = "inline-block";
    //   document.getElementById("localCard_mobile").style.top = "31%";
    //   document.getElementById("hoverShowLocal_mobile").style.bottom = "80%";
    //   document.getElementById("hoverShowLocal_mobile").style.zIndex = "-20";
      
      break;
    case 'account':
      document.getElementById("hoverShowAccount_mobile").style.zIndex = "20";
      document.getElementById("accountCard_mobile").style.display = "inline-block";
      document.getElementById("accountCard_mobile").style.top = "31%";
      document.getElementById("hoverShowAccount_mobile").style.bottom = "80%";
      document.getElementById("hoverShowAccount_mobile").style.zIndex = "-20";
      break;
    default:
      break;
    }
}

function closeMainCard() {
      // document.getElementById("localCard_mobile").style.display = "none";
      document.getElementById("leaderboardsCard_mobile").style.display = "none";
      document.getElementById("onlineCard_mobile").style.display = "none";
      document.getElementById("accountCard_mobile").style.display = "none";

      document.getElementById("mainCard_mobile").style.zIndex = "-25";
      document.getElementById("hoverShowAccount_mobile").style.zIndex = "20";
      document.getElementById("hoverShowOnline_mobile").style.zIndex = "20";
      // document.getElementById("hoverShowLocal_mobile").style.zIndex = "20";
      document.getElementById("hoverShowLeaderboards_mobile").style.zIndex = "20";
      
      // document.getElementById("hoverShowLocal_mobile").style.bottom = "66%";
      document.getElementById("hoverShowOnline_mobile").style.bottom = "49%";
      document.getElementById("hoverShowAccount_mobile").style.bottom = "32%";
      document.getElementById("hoverShowLeaderboards_mobile").style.bottom = "15%";

      document.getElementById("hoverShowAccount_mobile").style.height = "15%";
      document.getElementById("hoverShowLeaderboards_mobile").style.height = "15%";
      // document.getElementById("hoverShowLocal_mobile").style.height = "15%";
      document.getElementById("hoverShowOnline_mobile").style.height = "15%";

      setTimeout(function() {
      // document.getElementById("hoverShowLocal_mobile").innerHTML = "Local";
      document.getElementById("hoverShowOnline_mobile").innerHTML = "Online";
      document.getElementById("hoverShowAccount_mobile").innerHTML = "My Account";
      document.getElementById("hoverShowLeaderboards_mobile").innerHTML = "Leaderboards";
  }, 65);
}
