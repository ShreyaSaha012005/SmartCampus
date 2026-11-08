# SRMIST Smart Campus Management System

A complete IoT-integrated web application for SRM Institute of Science and Technology. Features a modern, responsive, glassmorphism UI built with Flask, MongoDB, and Python.

## 🚀 Features
1. **Smart Parking System** - View/Reserve slots.
2. **Classroom Monitoring** - IoT-controlled lights and fans.
3. **Smart Irrigation** - Soil moisture monitoring.
4. **Garbage Monitoring** - Bin fill level alerts.
5. **Smart Canteen** - Order food online (Demo mock).
6. **Seat Reservation** - Book seats across campus.
7. **Admin Dashboard** - Analytics and management.

## 🛠 Prerequisites
- Python 3.8+
- MongoDB Server (installed locally or running via Docker)

## ⚙️ Installation & Setup

1. **Install Dependencies:**
   Open your terminal/command prompt in the `smart campus` directory and run:
   ```bash
   pip install flask pymongo
   ```

2. **Database Setup (MongoDB):**
   - Ensure your MongoDB server is running locally on the default port (`localhost:27017`).
   - Run the provided setup script to automatically create the database (`smart_campus`), collections, and insert initial sample data:
     ```bash
     python setup_mongo.py
     ```
   
3. **Configure Database Connection:**
   - By default, the application connects to `mongodb://localhost:27017/`. You can change the `MONGO_URI` in `app.py` if your database is hosted elsewhere (e.g., MongoDB Atlas).
   - *Note: If the MongoDB connection fails, the application will automatically fall back to using "mock data" so you can still view the UI and test the features without a live database.*

4. **Run the Application:**
   ```bash
   python app.py
   ```
   
5. **Access the Website:**
   - Open your browser and go to: `http://127.0.0.1:5000`
   
## 🔐 Login Credentials
- **Admin**: Username: `admin` | Password: `admin123`
- **Student**: Username: `student1` | Password: `student123`
*(If DB is down/mock mode: admin/admin or student/student)*

## 📡 IoT Integration (ESP8266/Blynk API)
To send data from hardware (ESP8266/NodeMCU) to this web server:
- Endpoint: `POST http://<your-ip>:5000/api/update_sensor`
- JSON Payload Example: `{"sensor_type": "garbage", "id": "<mongodb_object_id_here>", "value": 85}`

## 🎨 UI Design
- Pure custom CSS with a modern **Glassmorphism** effect.
- Animated background gradient.
- Responsive mobile-friendly grid layouts.
- Dynamic data representation using charts (Chart.js).
