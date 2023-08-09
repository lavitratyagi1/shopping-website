var cartToggleButton = document.getElementById("cart-toggle-button");
var cartclosebutton = document.getElementById("cart-toggle-button.clicked");
var sidePanel = document.querySelector(".side-panel");
var cartOverlay = document.getElementById("cart-overlay");
var backgroundOverlay = document.getElementById("background-overlay");


var sidepanelclicked = false;


    
cartToggleButton.addEventListener("click", function() {
  sidePanel.classList.toggle("open");
  if (!sidepanelclicked) {
    cartToggleButton.classList.add("clicked");
    cartOverlay.style.display = sidePanel.classList.contains("open") ? "block" : "none";
  } else {
    cartToggleButton.classList.remove("clicked");
    cartOverlay.style.display = "none";
  }
  sidepanelclicked = !sidepanelclicked;
});

// Listner for add to cart button
const addToCartButtons = document.querySelectorAll(".add-to-cart-btn");
addToCartButtons.forEach((button) => {
  button.addEventListener("click", addToCart);
});

//Wishlist button
var heartIcon = document.getElementById("wishlist");
var wishlistclicked = false
heartIcon.addEventListener("click", function () {

    if (wishlistclicked) {
      heartIcon.classList.remove("clicked");
    } else {
      heartIcon.classList.add("clicked");
    }
  });