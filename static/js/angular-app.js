/**
 * TOURLY – AngularJS 1.8 Interactive Module (static/js/angular-app.js)
 * Uses custom interpolation symbols `[[ ]]` so AngularJS expressions coexist
 * cleanly alongside Django Template tags `{{ }}` without conflict.
 *
 * Demonstrates:
 * 1. Dynamic destination listing & live search/category filtering
 * 2. Two-way data binding (`ng-model`)
 * 3. Dynamic package price calculation & traveler roster management
 * 4. AngularJS controllers, filters, and expressions
 */

(function () {
    "use strict";
    if (typeof angular === "undefined") return;

    var app = angular.module("TourlyApp", []);

    // Configure [[ ]] interpolation to avoid clashing with Django {{ }}
    app.config(["$interpolateProvider", function ($interpolateProvider) {
        $interpolateProvider.startSymbol("[[");
        $interpolateProvider.endSymbol("]]");
    }]);

    /**
     * Controller 1: Interactive Destination Explorer & Budget Estimator (Homepage / Destinations)
     */
    app.controller("DestinationExplorerController", ["$scope", function ($scope) {
        $scope.searchKeyword = "";
        $scope.selectedCategory = "";
        $scope.travelersCount = 2;
        $scope.selectedTier = "Standard (4-Star)";
        $scope.tierMultiplier = 1.0;

        $scope.destinations = window.TOURLY_DESTINATIONS_DATA || [
            { id: 1, name: "Manali", country: "India", category: "Mountains", baseCost: 18500, description: "Snow-clad Pir Panjal peaks, Solang Valley adventure sports, and pine forests." },
            { id: 2, name: "Goa", country: "India", category: "Beaches", baseCost: 16800, description: "Golden Arabian Sea beaches, Portuguese heritage, and sunset cruises." },
            { id: 3, name: "Jaipur", country: "India", category: "Historical Places", baseCost: 11900, description: "Royal Rajputana Amber Fort, Hawa Mahal, and vibrant craft bazaars." },
            { id: 4, name: "Kashmir", country: "India", category: "Honeymoon", baseCost: 28500, description: "Dal Lake shikara rides, Mughal gardens, and Gulmarg alpine meadows." },
            { id: 5, name: "Kerala", country: "India", category: "Wildlife", baseCost: 22400, description: "Alleppey houseboats, Munnar tea gardens, and Periyar wildlife sanctuary." },
            { id: 6, name: "Shimla", country: "India", category: "Mountains", baseCost: 13500, description: "UNESCO Kalka-Shimla toy train, colonial Ridge promenade, and Kufri slopes." },
            { id: 7, name: "Dubai", country: "United Arab Emirates", category: "Adventure", baseCost: 54900, description: "Burj Khalifa observation deck, red dune desert safari, and Marina dhow cruise." },
            { id: 8, name: "Bali", country: "Indonesia", category: "Honeymoon", baseCost: 48900, description: "Ubud rice terraces, Uluwatu ocean temple, and Nusa Penida island coves." }
        ];

        $scope.categories = ["Adventure", "Beaches", "Mountains", "Historical Places", "Honeymoon", "Wildlife"];

        $scope.FilterDestination = function (dest) {
            var matchesKeyword = !$scope.searchKeyword ||
                dest.name.toLowerCase().indexOf($scope.searchKeyword.toLowerCase()) !== -1 ||
                dest.country.toLowerCase().indexOf($scope.searchKeyword.toLowerCase()) !== -1 ||
                dest.description.toLowerCase().indexOf($scope.searchKeyword.toLowerCase()) !== -1;

            var matchesCat = !$scope.selectedCategory || dest.category === $scope.selectedCategory;
            return matchesKeyword && matchesCat;
        };
    }]);

    /**
     * Controller 2: Interactive Package Price Calculator & Traveler Roster Manager (Booking / Packages)
     */
    app.controller("TripCalculatorController", ["$scope", function ($scope) {
        $scope.basePrice = window.TOURLY_BASE_PACKAGE_PRICE || 18500;
        $scope.packageName = window.TOURLY_PACKAGE_NAME || "Himalayan Snow & Solang Adventure";
        $scope.hotelUpgrade = "0";
        $scope.addAirportTransfer = true;
        $scope.addTravelInsurance = false;

        $scope.travelers = [
            { name: "Primary Traveler", age: 28, mealPref: "Vegetarian" },
            { name: "Companion Traveler", age: 26, mealPref: "Vegetarian" }
        ];

        $scope.newTravelerName = "";
        $scope.newTravelerAge = 25;
        $scope.newTravelerMeal = "Vegetarian";

        $scope.addTraveler = function () {
            if (!$scope.newTravelerName || !$scope.newTravelerName.trim()) return;
            if ($scope.travelers.length >= 15) return;
            $scope.travelers.push({
                name: $scope.newTravelerName.trim(),
                age: parseInt($scope.newTravelerAge, 10) || 25,
                mealPref: $scope.newTravelerMeal || "Vegetarian"
            });
            $scope.newTravelerName = "";
            // Sync with Django booking form input if present
            var djangoInput = document.getElementById("id_travelers");
            if (djangoInput) {
                djangoInput.value = $scope.travelers.length;
                if (window.updateBookingTotalPrice) window.updateBookingTotalPrice();
            }
        };

        $scope.removeTraveler = function (index) {
            if ($scope.travelers.length <= 1) return;
            $scope.travelers.splice(index, 1);
            var djangoInput = document.getElementById("id_travelers");
            if (djangoInput) {
                djangoInput.value = $scope.travelers.length;
                if (window.updateBookingTotalPrice) window.updateBookingTotalPrice();
            }
        };

        $scope.calculatePerPersonCost = function () {
            var perPerson = parseFloat($scope.basePrice) + parseFloat($scope.hotelUpgrade || 0);
            if ($scope.addAirportTransfer) perPerson += 1200;
            if ($scope.addTravelInsurance) perPerson += 850;
            return perPerson;
        };

        $scope.calculateGrandTotal = function () {
            return $scope.calculatePerPersonCost() * $scope.travelers.length;
        };
    }]);
})();
