-- ============================================================================
-- TOURLY – TRAVEL AGENCY MANAGEMENT AND BOOKING SYSTEM
-- MySQL Relational Database Schema (DDL) & Foreign Key Relationships
-- ============================================================================

CREATE DATABASE IF NOT EXISTS tourly_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE tourly_db;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS Users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Destinations Table
CREATE TABLE IF NOT EXISTS Destinations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE,
    country VARCHAR(100) NOT NULL DEFAULT 'India',
    category ENUM('Adventure', 'Beaches', 'Mountains', 'Historical Places', 'Honeymoon', 'Wildlife') NOT NULL,
    description TEXT NOT NULL,
    image VARCHAR(255) NOT NULL DEFAULT '/static/images/manali.svg',
    attractions TEXT NOT NULL
) ENGINE=InnoDB;

-- 3. TourPackages Table (Foreign Key -> Destinations.id)
CREATE TABLE IF NOT EXISTS TourPackages (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    destination_id BIGINT NOT NULL,
    package_name VARCHAR(180) NOT NULL,
    description TEXT NOT NULL,
    duration VARCHAR(60) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    image VARCHAR(255) NOT NULL DEFAULT '/static/images/manali.svg',
    hotel_info VARCHAR(255) NOT NULL DEFAULT '4-Star Deluxe Resort with Breakfast & Dinner',
    activities TEXT NOT NULL,
    itinerary TEXT NOT NULL,
    availability VARCHAR(180) NOT NULL DEFAULT 'Available Daily',
    CONSTRAINT fk_tourpackages_destination
        FOREIGN KEY (destination_id) REFERENCES Destinations(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 4. Bookings Table (Foreign Keys -> Users.id, TourPackages.id)
CREATE TABLE IF NOT EXISTS Bookings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    package_id BIGINT NOT NULL,
    customer_name VARCHAR(120) NOT NULL,
    customer_email VARCHAR(150) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    travel_date DATE NOT NULL,
    travelers INT UNSIGNED NOT NULL DEFAULT 2,
    total_price DECIMAL(12, 2) NOT NULL,
    special_requirements TEXT,
    booking_status ENUM('Pending', 'Confirmed', 'Cancelled', 'Completed') NOT NULL DEFAULT 'Pending',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bookings_user
        FOREIGN KEY (user_id) REFERENCES Users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_bookings_package
        FOREIGN KEY (package_id) REFERENCES TourPackages(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 5. ContactMessages Table
CREATE TABLE IF NOT EXISTS ContactMessages (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Indexes for fast searching and filtering
CREATE INDEX idx_destinations_category ON Destinations(category);
CREATE INDEX idx_packages_price ON TourPackages(price);
CREATE INDEX idx_bookings_status ON Bookings(booking_status);
