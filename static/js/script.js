/**
 * TOURLY – Vanilla JavaScript Module (static/js/script.js)
 * Demonstrates:
 * 1. Form Validation (Registration, Login, Booking, Contact)
 * 2. Password Visibility Toggle
 * 3. Image Gallery Modal & Lightbox Interaction
 * 4. Dynamic Price Calculation & Traveler Count Updates
 * 5. Confirmation Modal Dialogs & Custom Toast Notifications
 * 6. DOM Manipulation & Event Listeners
 */

(function () {
    "use strict";

    /**
     * Show a Bootstrap/DOM toast notification without using blocked browser alert()
     */
    window.showTourlyNotification = function (title, message, type) {
        var container = document.getElementById("tourlyToastContainer");
        if (!container) {
            container = document.createElement("div");
            container.id = "tourlyToastContainer";
            document.body.appendChild(container);
        }

        var borderClass = type === "error" ? "border-danger" : (type === "warning" ? "border-warning" : "border-info");
        var headerBg = type === "error" ? "#DC2626" : (type === "warning" ? "#D97706" : "#0A2540");

        var toastEl = document.createElement("div");
        toastEl.className = "toast show mb-2 shadow-lg border-0 " + borderClass;
        toastEl.setAttribute("role", "alert");
        toastEl.innerHTML =
            '<div class="toast-header text-white" style="background-color:' + headerBg + ';">' +
            '<strong class="me-auto">' + title + '</strong>' +
            '<small>Just now</small>' +
            '<button type="button" class="btn-close btn-close-white ms-2" aria-label="Close"></button>' +
            '</div>' +
            '<div class="toast-body bg-white text-dark fw-medium">' + message + '</div>';

        var closeBtn = toastEl.querySelector(".btn-close");
        if (closeBtn) {
            closeBtn.addEventListener("click", function () {
                toastEl.remove();
            });
        }

        container.appendChild(toastEl);
        setTimeout(function () {
            if (toastEl && toastEl.parentNode) {
                toastEl.remove();
            }
        }, 4500);
    };

    /**
     * Password Visibility Toggle
     */
    window.togglePasswordVisibility = function (inputId, iconId) {
        var input = document.getElementById(inputId);
        var icon = document.getElementById(iconId);
        if (!input) return;

        if (input.type === "password") {
            input.type = "text";
            if (icon) icon.textContent = "Hide";
        } else {
            input.type = "password";
            if (icon) icon.textContent = "Show";
        }
    };

    /**
     * Dynamic Booking Price Calculation & Traveler Stepper
     */
    window.updateBookingTotalPrice = function () {
        var priceEl = document.getElementById("basePackagePrice");
        var travelersInput = document.getElementById("id_travelers");
        var totalDisplay = document.getElementById("dynamicTotalPrice");
        var travelerCountBadge = document.getElementById("travelerCountBadge");

        if (!priceEl || !travelersInput || !totalDisplay) return;

        var basePrice = parseFloat(priceEl.getAttribute("data-price") || "0");
        var travelers = parseInt(travelersInput.value || "1", 10);

        if (isNaN(travelers) || travelers < 1) {
            travelers = 1;
            travelersInput.value = 1;
        } else if (travelers > 30) {
            travelers = 30;
            travelersInput.value = 30;
        }

        var total = basePrice * travelers;
        totalDisplay.textContent = "₹" + total.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        if (travelerCountBadge) {
            travelerCountBadge.textContent = travelers + (travelers === 1 ? " Traveler" : " Travelers");
        }
    };

    window.adjustTravelerCount = function (delta) {
        var travelersInput = document.getElementById("id_travelers");
        if (!travelersInput) return;
        var current = parseInt(travelersInput.value || "2", 10);
        var next = Math.min(30, Math.max(1, current + delta));
        travelersInput.value = next;
        window.updateBookingTotalPrice();
    };

    /**
     * Client-side Registration Form Validation
     */
    window.validateRegistrationForm = function (event) {
        var form = document.getElementById("registerForm");
        if (!form) return true;

        var fullName = document.getElementById("reg_full_name").value.trim();
        var email = document.getElementById("reg_email").value.trim();
        var phone = document.getElementById("reg_phone").value.trim();
        var password = document.getElementById("reg_password").value;
        var confirmPassword = document.getElementById("reg_confirm_password").value;
        var errorBox = document.getElementById("registerJsErrors");

        var errors = [];
        if (fullName.length < 3) {
            errors.push("Full name must be at least 3 characters long.");
        }
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            errors.push("Please enter a valid email address.");
        }
        var phoneRegex = /^[+0-9\-\s]{10,15}$/;
        if (!phoneRegex.test(phone)) {
            errors.push("Phone number must contain 10 to 15 digits.");
        }
        if (password.length < 8) {
            errors.push("Password must be at least 8 characters long.");
        }
        if (password !== confirmPassword) {
            errors.push("Password and Confirm Password do not match.");
        }

        if (errors.length > 0) {
            if (event) event.preventDefault();
            if (errorBox) {
                errorBox.classList.remove("d-none");
                errorBox.innerHTML = "<ul class='mb-0 ps-3'><li>" + errors.join("</li><li>") + "</li></ul>";
            }
            window.showTourlyNotification("Validation Error", errors[0], "error");
            return false;
        }
        if (errorBox) errorBox.classList.add("d-none");
        return true;
    };

    /**
     * Client-side Booking Form Validation
     */
    window.validateBookingForm = function (event) {
        var nameInput = document.getElementById("id_customer_name");
        var emailInput = document.getElementById("id_customer_email");
        var phoneInput = document.getElementById("id_customer_phone");
        var dateInput = document.getElementById("id_travel_date");
        var travelersInput = document.getElementById("id_travelers");
        var errorBox = document.getElementById("bookingJsErrors");

        if (!nameInput || !dateInput) return true;

        var errors = [];
        if (nameInput.value.trim().length < 3) {
            errors.push("Please enter the lead traveler's full name.");
        }
        if (!emailInput.value.includes("@")) {
            errors.push("Please provide a valid booking email.");
        }
        if (phoneInput.value.trim().length < 10) {
            errors.push("Please enter a valid 10-digit contact number.");
        }
        if (!dateInput.value) {
            errors.push("Please select a preferred travel date.");
        } else {
            var chosen = new Date(dateInput.value);
            var today = new Date();
            today.setHours(0, 0, 0, 0);
            if (chosen < today) {
                errors.push("Travel date cannot be in the past.");
            }
        }
        var count = parseInt(travelersInput.value, 10);
        if (isNaN(count) || count < 1 || count > 30) {
            errors.push("Number of travelers must be between 1 and 30.");
        }

        if (errors.length > 0) {
            if (event) event.preventDefault();
            if (errorBox) {
                errorBox.classList.remove("d-none");
                errorBox.innerHTML = "<ul class='mb-0 ps-3'><li>" + errors.join("</li><li>") + "</li></ul>";
            }
            window.showTourlyNotification("Booking Form Incomplete", errors[0], "error");
            return false;
        }
        if (errorBox) errorBox.classList.add("d-none");
        return true;
    };

    /**
     * Interactive Image Gallery Preview Switcher
     */
    window.switchGalleryImage = function (imageSrc, captionText) {
        var mainImg = document.getElementById("galleryMainImage");
        var captionEl = document.getElementById("galleryMainCaption");
        if (mainImg) {
            mainImg.src = imageSrc;
        }
        if (captionEl && captionText) {
            captionEl.textContent = captionText;
        }
    };

    /**
     * Attach DOM Event Listeners on Content Loaded
     */
    document.addEventListener("DOMContentLoaded", function () {
        var travelersInput = document.getElementById("id_travelers");
        if (travelersInput) {
            travelersInput.addEventListener("input", window.updateBookingTotalPrice);
            travelersInput.addEventListener("change", window.updateBookingTotalPrice);
            window.updateBookingTotalPrice();
        }

        var regForm = document.getElementById("registerForm");
        if (regForm) {
            regForm.addEventListener("submit", window.validateRegistrationForm);
        }

        var bookingForm = document.getElementById("bookingForm");
        if (bookingForm) {
            bookingForm.addEventListener("submit", window.validateBookingForm);
        }

        // Newsletter subscription handler on Homepage
        var newsletterForm = document.getElementById("newsletterForm");
        if (newsletterForm) {
            newsletterForm.addEventListener("submit", function (e) {
                e.preventDefault();
                var emailField = document.getElementById("newsletterEmail");
                if (emailField && emailField.value.includes("@")) {
                    window.showTourlyNotification(
                        "Subscribed!",
                        "Thank you! Exclusive Tourly travel deals will be sent to " + emailField.value + ".",
                        "info"
                    );
                    emailField.value = "";
                } else {
                    window.showTourlyNotification("Invalid Email", "Please enter a valid email address.", "error");
                }
            });
        }
    });
})();
