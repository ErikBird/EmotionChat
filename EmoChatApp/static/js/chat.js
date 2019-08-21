
var btnContainer = document.getElementById("user_list");

// Get all buttons with class="btn" inside the container
var btns = btnContainer.getElementsByClassName("btn");

// Loop through the buttons and add the active class to the current/clicked button
for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });}

/*
//@TODO: No Entries in Storage. Read Method is in chat.html
$(window).on("unload", function(e) {
    // Store all messages in client storage
    localStorage.setItem('{{receiver}}', JSON.stringify($("#messages")));
});*/