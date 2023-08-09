document.addEventListener("DOMContentLoaded", displayCartItems);

function displayCartItems() {
  const cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];

  const cartItemsContainer = document.getElementById("cart-items");
  cartItemsContainer.innerHTML = "";

  if (cartItems.length === 0) {
    cartItemsContainer.innerHTML = "<p>Your cart is empty.</p>";
    return;
  }

  cartItems.forEach((item) => {
    const cartItemDiv = document.createElement("div");
    cartItemDiv.innerHTML = `
      <p>${item.product} - Price: $${item.price} - Quantity: ${item.quantity}</p>
    `;
    cartItemsContainer.appendChild(cartItemDiv);
  });
}