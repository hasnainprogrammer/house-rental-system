// SELECTORS

const hamburgerMenu = document.querySelector(".hamburger-menu");
const navLinks = document.querySelector(".nav-links");
const dropdownLinkBtn = document.querySelectorAll(".dropdown-link-btn");
const dropdown = document.querySelectorAll(".dropdown");
const alert = document.querySelector(".alert");
const cancelIcon = document.querySelector(".cancel-icon");
const contactUsLink = document.querySelector(".contact-us-link");
const contactUsSection = document.querySelector(".contact-us");
const registerationPopupBtn = document.querySelector(
  ".registeration-popup-btn"
);
const registerationPopup = document.querySelector(".registeration-popup");
const registerationPopupCancelBtn = document.querySelector(
  ".registeration-popup-cancel-icon"
);
const overlay = document.querySelector(".overlay");
///////////////////////////////////////////////////////////////////

// Delete Property
const deleteBtn = document.querySelectorAll(".delete-btns");
deleteBtn.forEach((btn) => {
  btn.addEventListener("click", () => {
    const isDelete = confirm("Are you sure you want to delete this property?");
    if (isDelete) {
      const propertyId = btn.dataset.propertyid;
      window.location = "/accounts/manage_properties/delete/" + propertyId;
    }
  });
});
///////////////////////////////////////////////////////////////////

// EVENTS HANDLING

// Hamburger Menu
hamburgerMenu.addEventListener("click", () => {
  navLinks.classList.toggle("show-links");
});

// Alert
try {
  if (alert) {
    cancelIcon.addEventListener("click", () => {
      alert.classList.add("hide-alert");
      setTimeout(() => {
        alert.style.display = "none";
      }, 300);
    });

    setTimeout(() => {
      alert.classList.add("hide-alert");
      setTimeout(() => {
        alert.style.display = "none";
      }, 300);
    }, 5000);
  }
} catch {
  console.log("null");
}

// Dropdown
dropdownLinkBtn.forEach((btn, index) => {
  btn.addEventListener("click", () => {
    dropdown[index].classList.toggle("show-dropdown");
  });
});

// Contact Us
try {
  contactUsLink.addEventListener("click", () => {
    contactUsSection.scrollIntoView({ behavior: "smooth" });
  });
} catch {
  console.log("null");
}

// Registeration Popup
registerationPopupBtn.addEventListener("click", () => {
  if (registerationPopup.classList.contains("show-registeration-popup")) {
    registerationPopup.classList.remove("show-registeration-popup");
  } else {
    registerationPopup.classList.add("show-registeration-popup");
    overlay.classList.add("show-overlay");
  }
});

registerationPopupCancelBtn.addEventListener("click", () => {
  registerationPopup.classList.remove("show-registeration-popup");
  overlay.classList.remove("show-overlay");
});

///////////////////////////////////////////////////////////////////
