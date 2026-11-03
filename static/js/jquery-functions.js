/**
 * TOURLY – jQuery & AJAX Module (static/js/jquery-functions.js)
 * Demonstrates:
 * 1. CSRF Token Header Setup for Django AJAX POST requests
 * 2. Live Destination Search without reloading the page
 * 3. Dynamic Tour Package Filtering (Destination, Category, Budget, Sort)
 * 4. Asynchronous Package Details Modal Loading
 * 5. Asynchronous Contact Us Form Submission
 * 6. Booking Information Retrieval & Admin Booking Status Updates
 */

$(document).ready(function () {
    // Helper to extract Django CSRF token from cookies
    function getCsrfToken() {
        var cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            var cookies = document.cookie.split(";");
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === "csrftoken=") {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // 1. Live AJAX Destination Search on Destinations Page
    $("#ajaxDestinationSearchBtn, #ajaxDestinationInput, #ajaxDestinationCategory").on("keyup change click", function (e) {
        if (e.type === "click" && $(this).attr("id") !== "ajaxDestinationSearchBtn") {
            return;
        }
        var query = $("#ajaxDestinationInput").val() || "";
        var category = $("#ajaxDestinationCategory").val() || "";
        var container = $("#ajaxDestinationsGrid");
        if (!container.length) return;

        $.ajax({
            url: "/api/destinations/search/",
            method: "GET",
            data: { q: query, category: category },
            dataType: "json",
            success: function (response) {
                if (response.status === "ok") {
                    $("#destinationResultCount").text(response.count);
                    container.empty();
                    if (response.destinations.length === 0) {
                        container.html(
                            '<div class="col-12"><div class="alert alert-light border text-center py-4">' +
                            '<h5>No destinations matched your filter criteria.</h5>' +
                            '<p class="text-muted mb-0">Try clearing the search box or choosing another travel category.</p>' +
                            '</div></div>'
                        );
                        return;
                    }
                    $.each(response.destinations, function (idx, d) {
                        var attractionsHtml = "";
                        $.each(d.attractions.slice(0, 3), function (i, attr) {
                            attractionsHtml += '<span class="badge bg-light text-dark border me-1 mb-1">' + attr + '</span>';
                        });
                        var cardHtml =
                            '<div class="col-md-6 col-lg-4">' +
                            '<div class="card tourly-card">' +
                            '<div class="card-img-wrapper">' +
                            '<img src="' + d.image + '" class="card-img-top" alt="' + d.name + '">' +
                            '<span class="category-badge">' + d.category + '</span>' +
                            '</div>' +
                            '<div class="card-body d-flex flex-column">' +
                            '<div class="d-flex justify-content-between align-items-center mb-2">' +
                            '<h5 class="card-title fw-bold mb-0" style="color:#0A2540;">' + d.name + '</h5>' +
                            '<span class="text-muted small"><i class="bi bi-geo-alt-fill text-info"></i> ' + d.country + '</span>' +
                            '</div>' +
                            '<p class="card-text text-muted small flex-grow-1">' + d.description + '</p>' +
                            '<div class="mb-3">' + attractionsHtml + '</div>' +
                            '<a href="' + d.detail_url + '" class="btn btn-tourly-navy w-100">Explore ' + d.name + '</a>' +
                            '</div></div></div>';
                        container.append(cardHtml);
                    });
                }
            }
        });
    });

    // 2. Dynamic AJAX Tour Package Filtering
    $("#ajaxPackageFilterForm select, #ajaxPackageFilterForm input").on("change keyup", function () {
        var formData = $("#ajaxPackageFilterForm").serialize();
        var grid = $("#ajaxPackagesGrid");
        if (!grid.length) return;

        $.ajax({
            url: "/api/packages/filter/",
            method: "GET",
            data: formData,
            dataType: "json",
            success: function (response) {
                if (response.status === "ok") {
                    $("#packageResultCount").text(response.count);
                    grid.empty();
                    if (response.packages.length === 0) {
                        grid.html(
                            '<div class="col-12"><div class="alert alert-light border text-center py-5">' +
                            '<h5>No tour packages found within the selected filter criteria.</h5>' +
                            '<p class="text-muted mb-0">Try increasing your maximum budget or selecting All Destinations.</p>' +
                            '</div></div>'
                        );
                        return;
                    }
                    $.each(response.packages, function (i, pkg) {
                        var formattedPrice = "₹" + Number(pkg.price).toLocaleString("en-IN");
                        var card =
                            '<div class="col-md-6 col-lg-4">' +
                            '<div class="card tourly-card">' +
                            '<div class="card-img-wrapper">' +
                            '<img src="' + pkg.image + '" class="card-img-top" alt="' + pkg.package_name + '">' +
                            '<span class="category-badge">' + pkg.category + '</span>' +
                            '<span class="price-badge">' + formattedPrice + '</span>' +
                            '</div>' +
                            '<div class="card-body d-flex flex-column">' +
                            '<div class="small text-info fw-semibold mb-1">' + pkg.destination_name + ' • ' + pkg.duration + '</div>' +
                            '<h5 class="card-title fw-bold" style="color:#0A2540;">' + pkg.package_name + '</h5>' +
                            '<p class="card-text text-muted small flex-grow-1">' + pkg.description + '</p>' +
                            '<div class="small text-secondary mb-3"><strong>Hotel:</strong> ' + pkg.hotel_info + '</div>' +
                            '<div class="d-flex gap-2 mt-auto">' +
                            '<button type="button" class="btn btn-outline-dark btn-sm flex-grow-1 ajax-quick-view-btn" data-pkg-id="' + pkg.id + '">Quick View</button>' +
                            '<a href="' + pkg.detail_url + '" class="btn btn-tourly-turquoise btn-sm flex-grow-1">Details</a>' +
                            '<a href="' + pkg.book_url + '" class="btn btn-tourly-orange btn-sm flex-grow-1">Book Now</a>' +
                            '</div></div></div></div>';
                        grid.append(card);
                    });
                }
            }
        });
    });

    // 3. Load Package Details Asynchronously into Bootstrap Modal
    $(document).on("click", ".ajax-quick-view-btn", function () {
        var pkgId = $(this).data("pkg-id");
        $.ajax({
            url: "/api/packages/" + pkgId + "/",
            method: "GET",
            dataType: "json",
            success: function (res) {
                if (res.status === "ok") {
                    var p = res.package;
                    $("#modalPkgTitle").text(p.package_name);
                    $("#modalPkgSubtitle").text(p.destination_name + ", " + p.country + " | " + p.duration + " | " + p.category);
                    $("#modalPkgPrice").text("₹" + Number(p.price).toLocaleString("en-IN") + " / person");
                    $("#modalPkgDesc").text(p.description);
                    $("#modalPkgHotel").text(p.hotel_info);
                    $("#modalPkgAvailability").text(p.availability);
                    $("#modalPkgBookBtn").attr("href", p.book_url);

                    var itinList = $("#modalPkgItinerary").empty();
                    $.each(p.itinerary, function (idx, dayText) {
                        itinList.append('<li class="list-group-item small">' + dayText + '</li>');
                    });

                    var modalEl = document.getElementById("packageQuickViewModal");
                    if (modalEl && window.bootstrap) {
                        var modal = new bootstrap.Modal(modalEl);
                        modal.show();
                    }
                }
            }
        });
    });

    // 4. Submit Contact Us Form Asynchronously via jQuery AJAX
    $("#ajaxContactSubmitBtn").on("click", function (e) {
        e.preventDefault();
        var form = $("#contactUsForm");
        var statusBox = $("#ajaxContactResponse");

        $.ajax({
            url: "/api/contact/submit/",
            method: "POST",
            headers: { "X-CSRFToken": getCsrfToken() },
            data: form.serialize(),
            dataType: "json",
            success: function (res) {
                if (res.status === "ok") {
                    statusBox
                        .removeClass("d-none alert-danger")
                        .addClass("alert-success")
                        .html("<strong>Success!</strong> " + res.message);
                    form[0].reset();
                    if (window.showTourlyNotification) {
                        window.showTourlyNotification("Inquiry Stored", res.message, "info");
                    }
                }
            },
            error: function (xhr) {
                var errText = "Please check all contact form fields (message must be at least 10 characters).";
                if (xhr.responseJSON && xhr.responseJSON.errors) {
                    errText = JSON.stringify(xhr.responseJSON.errors);
                }
                statusBox
                    .removeClass("d-none alert-success")
                    .addClass("alert-danger")
                    .html("<strong>Validation Error:</strong> " + errText);
            }
        });
    });

    // 5. Retrieve Booking Details via AJAX on Customer/Admin Dashboard
    $(document).on("click", ".ajax-view-booking-btn", function () {
        var bookingId = $(this).data("booking-id");
        $.ajax({
            url: "/api/bookings/" + bookingId + "/",
            method: "GET",
            dataType: "json",
            success: function (res) {
                if (res.status === "ok") {
                    var b = res.booking;
                    $("#modalBookingId").text("#" + b.id);
                    $("#modalBookingCustomer").text(b.customer_name + " (" + b.customer_email + " | " + b.customer_phone + ")");
                    $("#modalBookingPackage").text(b.package_name + " (" + b.destination_name + ")");
                    $("#modalBookingDate").text(b.travel_date + " • " + b.duration);
                    $("#modalBookingTravelers").text(b.travelers + " Traveler(s)");
                    $("#modalBookingTotal").text("₹" + Number(b.total_price).toLocaleString("en-IN"));
                    $("#modalBookingRequirements").text(b.special_requirements);
                    $("#modalBookingStatus").text(b.booking_status);

                    var modalEl = document.getElementById("bookingDetailModal");
                    if (modalEl && window.bootstrap) {
                        var modal = new bootstrap.Modal(modalEl);
                        modal.show();
                    }
                }
            }
        });
    });

    // 6. Admin Dynamic Booking Status Update via jQuery AJAX
    $(document).on("change", ".ajax-admin-status-select", function () {
        var bookingId = $(this).data("booking-id");
        var newStatus = $(this).val();
        var badgeEl = $("#statusBadge_" + bookingId);

        $.ajax({
            url: "/api/admin/booking-status/",
            method: "POST",
            headers: { "X-CSRFToken": getCsrfToken() },
            data: { booking_id: bookingId, booking_status: newStatus },
            dataType: "json",
            success: function (res) {
                if (res.status === "ok") {
                    badgeEl
                        .removeClass("badge-status-Pending badge-status-Confirmed badge-status-Cancelled badge-status-Completed")
                        .addClass("badge-status-" + res.new_status)
                        .text(res.new_status);
                    if (window.showTourlyNotification) {
                        window.showTourlyNotification("Booking Updated", res.message, "info");
                    }
                }
            }
        });
    });
});
