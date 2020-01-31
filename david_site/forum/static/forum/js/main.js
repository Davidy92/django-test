function hide(authorized, loggedIn, postUser, element){
  var hide = document.querySelector(element);
  if( authorized == 'false' || loggedIn != postUser){
    hide.style.display = 'none';
  }
}

function hide_like(authorized, loggedIn, postUser, element){
  var hide = document.querySelector(element);
  console.log(authorized, loggedIn, postUser, element);
  if( authorized == 'false' || loggedIn == postUser){
    hide.style.display = 'none';
  }
}

function hide_comment(authorized, element){
  var hide = document.querySelector(element);
  if( authorized == 'false'){
    hide.style.display = 'none';
  }
}


function startTime(element) {
  var today = new Date();
  var date_split = today.toLocaleString().split(" ");
  var time = date_split[1] + " " + date_split[2];
  document.getElementById(element).innerHTML = time;

  setTimeout(function() { startTime(element); } , 500);
}

// function hide_log(authorized, parent, element){
//   var hide = document.getElementById(element);
//   console.log(hide);
//   if (authorized == "true") {
//     // hide.querySelector(element).innerHTML = "<a href=\"{% url 'logout' %}\">Logout</a>";
//     hide.innerHTML = "<a href=\"{% url 'logout' %}\">Logout</a>";
//   }
//   else if (authorized == "false"){
//     // hide.querySelector(element).innerHTML = "<a href=\"{% url 'login' %}\">Login</a>";
//     hide.innerHTML = "<a href=\"{% url 'login' %}\">Login</a>";
//   }
// }
