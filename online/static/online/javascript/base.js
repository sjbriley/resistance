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