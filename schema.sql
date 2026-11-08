CREATE DATABASE IF NOT EXISTS smart_campus;
USE smart_campus;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'admin') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS parking_slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slot_name VARCHAR(20) NOT NULL UNIQUE,
    status ENUM('Free', 'Occupied') DEFAULT 'Free',
    reserved_by INT DEFAULT NULL,
    FOREIGN KEY (reserved_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS classrooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(20) NOT NULL UNIQUE,
    usage_status ENUM('Free', 'Occupied') DEFAULT 'Free',
    lights_status ENUM('ON', 'OFF') DEFAULT 'OFF',
    fans_status ENUM('ON', 'OFF') DEFAULT 'OFF'
);

CREATE TABLE IF NOT EXISTS irrigation_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    area_name VARCHAR(50) NOT NULL,
    moisture_level INT NOT NULL, -- Percentage 0-100
    pump_status ENUM('ON', 'OFF') DEFAULT 'OFF',
    mode ENUM('Auto', 'Manual') DEFAULT 'Auto',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS garbage_bins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(50) NOT NULL,
    fill_level INT NOT NULL, -- Percentage 0-100
    status ENUM('Normal', 'Full') DEFAULT 'Normal'
);

CREATE TABLE IF NOT EXISTS food_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('Pending', 'Preparing', 'Ready', 'Completed') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS seat_reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    venue ENUM('Library', 'Canteen', 'Seminar Hall') NOT NULL,
    seat_number VARCHAR(20) NOT NULL,
    reservation_time DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert Sample Data
INSERT IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin');
INSERT IGNORE INTO users (username, password, role) VALUES ('student1', 'student123', 'student');

INSERT IGNORE INTO parking_slots (slot_name, status) VALUES ('P1', 'Free'), ('P2', 'Occupied'), ('P3', 'Free'), ('P4', 'Free'), ('P5', 'Occupied');
INSERT IGNORE INTO classrooms (room_number, usage_status, lights_status, fans_status) VALUES ('Room 101', 'Occupied', 'ON', 'ON'), ('Room 102', 'Free', 'OFF', 'OFF'), ('Room 103', 'Occupied', 'ON', 'OFF');
INSERT IGNORE INTO irrigation_data (area_name, moisture_level, pump_status, mode) VALUES ('Main Garden', 45, 'OFF', 'Auto'), ('Sports Field', 20, 'ON', 'Auto');
INSERT IGNORE INTO garbage_bins (location, fill_level, status) VALUES ('Main Gate', 30, 'Normal'), ('Canteen', 95, 'Full'), ('Library', 50, 'Normal');
INSERT IGNORE INTO food_items (name, price, description, available) VALUES ('Veg Burger', 50.00, 'Delicious veg burger', TRUE), ('Cold Coffee', 40.00, 'Refreshing cold coffee', TRUE), ('French Fries', 35.00, 'Crispy fries', TRUE);
