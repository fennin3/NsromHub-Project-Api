

// Get the modal for the member of parliament
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

//Get the modalContent
var modalContent = document.getElementById("modalContent");
// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event1) {
  if (event1.target == modal) {
    modal.style.display = "none";
  }
  
}














// Get the modal for the member of parliament
var modal2 = document.getElementById("myModal-2");

// Get the button that opens the modal
var btn2 = document.getElementById("myBtn-2");

// Get the <span> element that closes the modal
var span2 = document.getElementsByClassName("close-2")[0];

// When the user clicks on the button, open the modal
btn2.onclick = function() {
  modal2.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span2.onclick = function() {
  modal2.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event2) {
  if (event2.target == modal2) {
    modal2.style.display = "none";
  }
  
}