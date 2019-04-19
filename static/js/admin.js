var header;
var sticky;

window.onscroll = function() {fixedHeader()};
window.onload = function() {
    // HEADER JS
    header = document.getElementById("header-fixed");
    sticky = header.offsetTop;

    var table = document.getElementById("table-surveys");
    if(table != null) {
      // var divTemp = document.createAttribute('div');
      // // divTemp.setAttribute('id', 'filter-container');
      // // var filterTemp =
      // // divTemp.appendChild(filterTemp);

      $('#table-surveys').DataTable();
      $('#table-surveys_filter input').attr("placeholder", "Search survey data...");
    }
}

function openUsers(evt, usersName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(usersName).style.display = "block";
  evt.currentTarget.className += " active";
}


/* JS FOR HEADER */
function fixedHeader() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
}