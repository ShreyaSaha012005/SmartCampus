from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
from datetime import datetime
import os
import random

app = Flask(__name__)
app.secret_key = 'smart_campus_secret_key'

# MongoDB Configuration
MONGO_URI = 'mongodb://localhost:27017/'

MOCK_PARKING_SLOTS = [
    {'slot_name': 'P1', 'status': 'Free', 'reserved_by': None},
    {'slot_name': 'P2', 'status': 'Occupied', 'reserved_by': 'student1'},
    {'slot_name': 'P3', 'status': 'Free', 'reserved_by': None},
    {'slot_name': 'P4', 'status': 'Occupied', 'reserved_by': 'admin'},
    {'slot_name': 'P5', 'status': 'Free', 'reserved_by': None},
]

MOCK_CLASSROOMS = [
    {'room_number': 'Room 101', 'usage_status': 'Occupied', 'lights_status': 'ON', 'fans_status': 'ON'},
    {'room_number': 'Room 102', 'usage_status': 'Free', 'lights_status': 'OFF', 'fans_status': 'OFF'},
    {'room_number': 'Room 103', 'usage_status': 'Occupied', 'lights_status': 'ON', 'fans_status': 'OFF'},
]

MOCK_IRRIGATION = [
    {'area_name': 'Main Garden', 'moisture_level': 45, 'pump_status': 'OFF', 'mode': 'Auto', 'last_updated': datetime.now()},
    {'area_name': 'Sports Field', 'moisture_level': 22, 'pump_status': 'ON', 'mode': 'Auto', 'last_updated': datetime.now()},
    {'area_name': 'Flower Beds', 'moisture_level': 60, 'pump_status': 'OFF', 'mode': 'Manual', 'last_updated': datetime.now()},
]

MOCK_GARBAGE = [
    {'location': 'Main Gate', 'fill_level': 30, 'status': 'Normal'},
    {'location': 'Canteen', 'fill_level': 92, 'status': 'Full'},
    {'location': 'Library', 'fill_level': 52, 'status': 'Normal'},
]

MOCK_CATEGORIES = {
    'Starters': [
        {'category': 'Starters', 'name': 'Paneer Tikka', 'price': 120.00, 'description': 'Grilled cottage cheese cubes marinated in spices', 'available': True},
        {'category': 'Starters', 'name': 'Crispy Corn', 'price': 90.00, 'description': 'Fried sweet corn tossed with pepper and salt', 'available': True},
        {'category': 'Starters', 'name': 'Chicken 65', 'price': 150.00, 'description': 'Spicy, deep-fried chicken bites', 'available': True},
    ],
    'Main Course': [
        {'category': 'Main Course', 'name': 'Veg Biryani', 'price': 180.00, 'description': 'Aromatic rice dish cooked with mixed vegetables and spices', 'available': True},
        {'category': 'Main Course', 'name': 'Chicken Biryani', 'price': 220.00, 'description': 'Classic Hyderabadi style chicken dum biryani', 'available': True},
        {'category': 'Main Course', 'name': 'Butter Naan & Paneer Masala', 'price': 200.00, 'description': 'Rich paneer gravy served with butter naan', 'available': True},
    ],
    'Fast Food': [
        {'category': 'Fast Food', 'name': 'Veg Burger', 'price': 60.00, 'description': 'Classic veg patty burger with cheese', 'available': True},
        {'category': 'Fast Food', 'name': 'French Fries', 'price': 50.00, 'description': 'Crispy golden potato fries', 'available': True},
        {'category': 'Fast Food', 'name': 'Chicken Burger', 'price': 90.00, 'description': 'Crispy chicken patty with fresh lettuce', 'available': True},
    ],
    'Beverages': [
        {'category': 'Beverages', 'name': 'Cold Coffee', 'price': 60.00, 'description': 'Refreshing iced coffee with a scoop of ice cream', 'available': True},
        {'category': 'Beverages', 'name': 'Mango Lassi', 'price': 50.00, 'description': 'Sweet yogurt drink blended with fresh mango pulp', 'available': True},
        {'category': 'Beverages', 'name': 'Fresh Lime Soda', 'price': 40.00, 'description': 'Chilled sweet and salt lime soda', 'available': True},
    ],
    'Desserts': [
        {'category': 'Desserts', 'name': 'Gulab Jamun (2 pcs)', 'price': 40.00, 'description': 'Soft milk-solid dumplings soaked in sugar syrup', 'available': True},
        {'category': 'Desserts', 'name': 'Chocolate Brownie with Ice Cream', 'price': 100.00, 'description': 'Warm brownie topped with vanilla ice cream', 'available': True},
    ],
}

MOCK_LIBRARY_BOOKS = [
    {'title': 'Introduction to Algorithms', 'author': 'Thomas H. Cormen', 'total_copies': 5, 'available_copies': 3},
    {'title': 'Clean Code', 'author': 'Robert C. Martin', 'total_copies': 3, 'available_copies': 2},
    {'title': 'Design Patterns', 'author': 'Erich Gamma', 'total_copies': 4, 'available_copies': 1},
    {'title': 'Computer Networks', 'author': 'Andrew S. Tanenbaum', 'total_copies': 6, 'available_copies': 4},
]

MOCK_LIBRARY_BORROWINGS = [
    {'student_name': 'student1', 'book_title': 'Introduction to Algorithms', 'borrow_date': 'Today', 'status': 'Borrowed'},
    {'student_name': 'student2', 'book_title': 'Clean Code', 'borrow_date': 'Today', 'status': 'Borrowed'},
    {'student_name': 'student3', 'book_title': 'Design Patterns', 'borrow_date': 'Yesterday', 'status': 'Borrowed'},
]


def get_db():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        return client['smart_campus']
    except ConnectionFailure:
        print("Error: Could not connect to MongoDB.")
        return None


def ensure_demo_data():
    db = get_db()
    if db is None:
        return

    collections = {
        'users': [
            {'username': 'admin', 'password': 'admin123', 'role': 'admin', 'created_at': datetime.now()},
            {'username': 'student1', 'password': 'student123', 'role': 'student', 'created_at': datetime.now()},
        ],
        'parking_slots': [
            {'slot_name': 'P1', 'status': 'Free', 'reserved_by': None},
            {'slot_name': 'P2', 'status': 'Occupied', 'reserved_by': 'student1'},
            {'slot_name': 'P3', 'status': 'Free', 'reserved_by': None},
            {'slot_name': 'P4', 'status': 'Occupied', 'reserved_by': 'admin'},
            {'slot_name': 'P5', 'status': 'Free', 'reserved_by': None},
        ],
        'classrooms': [
            {'room_number': 'Room 101', 'usage_status': 'Occupied', 'lights_status': 'ON', 'fans_status': 'ON'},
            {'room_number': 'Room 102', 'usage_status': 'Free', 'lights_status': 'OFF', 'fans_status': 'OFF'},
            {'room_number': 'Room 103', 'usage_status': 'Occupied', 'lights_status': 'ON', 'fans_status': 'OFF'},
        ],
        'irrigation_data': [
            {'area_name': 'Main Garden', 'moisture_level': 45, 'pump_status': 'OFF', 'mode': 'Auto', 'last_updated': datetime.now()},
            {'area_name': 'Sports Field', 'moisture_level': 22, 'pump_status': 'ON', 'mode': 'Auto', 'last_updated': datetime.now()},
        ],
        'garbage_bins': [
            {'location': 'Main Gate', 'fill_level': 30, 'status': 'Normal'},
            {'location': 'Canteen', 'fill_level': 92, 'status': 'Full'},
            {'location': 'Library', 'fill_level': 52, 'status': 'Normal'},
        ],
        'food_items': [
            {'category': 'Starters', 'name': 'Paneer Tikka', 'price': 120.00, 'description': 'Grilled cottage cheese cubes marinated in spices', 'available': True},
            {'category': 'Main Course', 'name': 'Veg Biryani', 'price': 180.00, 'description': 'Aromatic rice dish cooked with mixed vegetables and spices', 'available': True},
            {'category': 'Fast Food', 'name': 'Veg Burger', 'price': 60.00, 'description': 'Classic veg patty burger with cheese', 'available': True},
            {'category': 'Beverages', 'name': 'Cold Coffee', 'price': 60.00, 'description': 'Refreshing iced coffee with a scoop of ice cream', 'available': True},
            {'category': 'Desserts', 'name': 'Gulab Jamun (2 pcs)', 'price': 40.00, 'description': 'Soft milk-solid dumplings soaked in sugar syrup', 'available': True},
        ],
        'library_books': [
            {'title': 'Introduction to Algorithms', 'author': 'Thomas H. Cormen', 'total_copies': 5, 'available_copies': 3},
            {'title': 'Clean Code', 'author': 'Robert C. Martin', 'total_copies': 3, 'available_copies': 2},
            {'title': 'Computer Networks', 'author': 'Andrew S. Tanenbaum', 'total_copies': 6, 'available_copies': 4},
        ],
        'library_borrowings': [
            {'student_name': 'student1', 'book_title': 'Introduction to Algorithms', 'borrow_date': datetime.now(), 'status': 'Borrowed'},
            {'student_name': 'student2', 'book_title': 'Clean Code', 'borrow_date': datetime.now(), 'status': 'Borrowed'},
        ],
    }

    for collection_name, documents in collections.items():
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
        if db[collection_name].count_documents({}) == 0:
            db[collection_name].insert_many(documents)

    if 'seat_reservations' not in db.list_collection_names():
        db.create_collection('seat_reservations')


def simulate_sensor_data():
    db = get_db()
    if db is None:
        return

    # Keep sensor changes gradual and realistic, like live IoT telemetry.
    for slot in db.parking_slots.find():
        current = slot.get('status', 'Free')
        flip_chance = random.random()
        if flip_chance < 0.08:
            new_status = 'Occupied' if current == 'Free' else 'Free'
            db.parking_slots.update_one(
                {'_id': slot['_id']},
                {'$set': {'status': new_status, 'reserved_by': None if new_status == 'Free' else 'iot_sensor', 'last_updated': datetime.now()}}
            )

    for room in db.classrooms.find():
        usage = room.get('usage_status', 'Free')
        if random.random() < 0.12:
            usage = 'Occupied' if usage == 'Free' else 'Free'

        lights = room.get('lights_status', 'OFF')
        if random.random() < 0.10:
            lights = 'ON' if lights == 'OFF' else 'OFF'

        fans = room.get('fans_status', 'OFF')
        if random.random() < 0.10:
            fans = 'ON' if fans == 'OFF' else 'OFF'

        db.classrooms.update_one(
            {'_id': room['_id']},
            {'$set': {'usage_status': usage, 'lights_status': lights, 'fans_status': fans, 'last_updated': datetime.now()}}
        )

    for area in db.irrigation_data.find():
        current_moisture = int(area.get('moisture_level', 50))
        drift = random.randint(-8, 8)
        moisture = max(10, min(95, current_moisture + drift))
        pump = 'ON' if moisture < 35 else 'OFF'
        db.irrigation_data.update_one(
            {'_id': area['_id']},
            {'$set': {'moisture_level': moisture, 'pump_status': pump, 'mode': 'Auto', 'last_updated': datetime.now()}}
        )

    for bin_doc in db.garbage_bins.find():
        current_fill = int(bin_doc.get('fill_level', 30))
        delta = random.randint(-6, 8)
        fill = max(5, min(99, current_fill + delta))
        status = 'Full' if fill >= 80 else 'Normal'
        db.garbage_bins.update_one(
            {'_id': bin_doc['_id']},
            {'$set': {'fill_level': fill, 'status': status, 'last_updated': datetime.now()}}
        )

    if 'seat_reservations' in db.list_collection_names() and db.seat_reservations.count_documents({}) == 0:
        db.seat_reservations.insert_many([
            {'user_id': 'demo_user_1', 'venue': 'Main Library', 'seat_number': 'A12', 'reservation_time': '10:00 AM', 'created_at': datetime.now()},
            {'user_id': 'demo_user_2', 'venue': 'CSE Block', 'seat_number': 'B07', 'reservation_time': '02:30 PM', 'created_at': datetime.now()}
        ])


ensure_demo_data()
simulate_sensor_data()

# Context processor to inject user role into templates
@app.context_processor
def inject_user():
    return dict(session=session)

# ----------------- ROUTES -----------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        if db is not None:
            user = db.users.find_one({"username": username, "password": password})
            if user:
                session['user_id'] = str(user['_id'])
                session['username'] = user['username']
                session['role'] = user.get('role', 'student')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'error')
        else:
            # Fallback for demo without DB
            if username == 'admin' and password == 'admin':
                session['user_id'] = 'mock_admin_id'
                session['username'] = 'admin'
                session['role'] = 'admin'
                return redirect(url_for('dashboard'))
            elif username == 'student' and password == 'student':
                session['user_id'] = 'mock_student_id'
                session['username'] = 'student'
                session['role'] = 'student'
                return redirect(url_for('dashboard'))
            flash('Database connection failed. Used fallback credentials (admin/admin or student/student). Invalid.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'student')
        
        db = get_db()
        if db is not None:
            if db.users.find_one({"username": username}):
                flash('Username already exists.', 'error')
            else:
                db.users.insert_one({
                    "username": username,
                    "password": password,
                    "role": role,
                    "created_at": datetime.now()
                })
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
        else:
            flash('Database connection failed. Cannot register.', 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/parking')
def parking():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    slots = []
    db = get_db()
    if db is not None and 'parking_slots' in db.list_collection_names() and db.parking_slots.count_documents({}) > 0:
        slots_cursor = db.parking_slots.find()
        for slot in slots_cursor:
            slot['id'] = str(slot['_id'])
            slots.append(slot)
    else:
        slots = [
            {'id': '1', 'slot_name': 'P1', 'status': 'Free'},
            {'id': '2', 'slot_name': 'P2', 'status': 'Occupied'},
            {'id': '3', 'slot_name': 'P3', 'status': 'Free'},
            {'id': '4', 'slot_name': 'P4', 'status': 'Occupied'},
            {'id': '5', 'slot_name': 'P5', 'status': 'Free'}
        ]
    return render_template('parking.html', slots=slots)

@app.route('/reserve_parking', methods=['POST'])
def reserve_parking():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    slot_id = data.get('slot_id')
    
    db = get_db()
    if db is not None:
        result = db.parking_slots.update_one(
            {'_id': ObjectId(slot_id)},
            {'$set': {'status': 'Occupied', 'reserved_by': session['user_id']}}
        )
        if result.modified_count > 0:
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Slot not found or already occupied.'})
    return jsonify({'success': True, 'message': 'Mock reserved'})

@app.route('/classroom')
def classroom():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    rooms = []
    db = get_db()
    if db is not None and 'classrooms' in db.list_collection_names() and db.classrooms.count_documents({}) > 0:
        rooms_cursor = db.classrooms.find()
        for room in rooms_cursor:
            room['id'] = str(room['_id'])
            rooms.append(room)
    else:
        rooms = [
            {'id': '1', 'room_number': 'Room 101', 'usage_status': 'Occupied', 'lights_status': 'ON', 'fans_status': 'ON'},
            {'id': '2', 'room_number': 'Room 102', 'usage_status': 'Free', 'lights_status': 'OFF', 'fans_status': 'OFF'},
            {'id': '3', 'room_number': 'Room 103', 'usage_status': 'Occupied', 'lights_status': 'ON', 'fans_status': 'OFF'}
        ]
    return render_template('classroom.html', rooms=rooms)

@app.route('/toggle_device', methods=['POST'])
def toggle_device():
    # Simulated IoT control endpoint
    data = request.json
    room_id = data.get('room_id')
    device = data.get('device')
    new_status = data.get('status')
    
    db = get_db()
    if db is not None:
        field = 'lights_status' if device == 'lights' else 'fans_status'
        db.classrooms.update_one(
            {'_id': ObjectId(room_id)},
            {'$set': {field: new_status}}
        )
    # In a real scenario, we would also call ESP8266/Blynk API here.
    return jsonify({'success': True, 'message': f'{device} turned {new_status}'})

@app.route('/irrigation')
def irrigation():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    data = []
    db = get_db()
    if db is not None and 'irrigation_data' in db.list_collection_names() and db.irrigation_data.count_documents({}) > 0:
        areas_cursor = db.irrigation_data.find()
        for area in areas_cursor:
            area['id'] = str(area['_id'])
            data.append(area)
    else:
        data = [
            {'id': '1', 'area_name': 'Main Garden', 'moisture_level': 45, 'pump_status': 'OFF', 'mode': 'Auto'},
            {'id': '2', 'area_name': 'Sports Field', 'moisture_level': 22, 'pump_status': 'ON', 'mode': 'Auto'},
            {'id': '3', 'area_name': 'Flower Beds', 'moisture_level': 60, 'pump_status': 'OFF', 'mode': 'Manual'}
        ]
    return render_template('irrigation.html', areas=data)

@app.route('/garbage')
def garbage():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    bins = []
    db = get_db()
    if db is not None and 'garbage_bins' in db.list_collection_names() and db.garbage_bins.count_documents({}) > 0:
        bins_cursor = db.garbage_bins.find()
        for bin_doc in bins_cursor:
            bin_doc['id'] = str(bin_doc['_id'])
            bins.append(bin_doc)
    else:
        bins = [
            {'id': '1', 'location': 'Main Gate', 'fill_level': 30, 'status': 'Normal'},
            {'id': '2', 'location': 'Canteen', 'fill_level': 92, 'status': 'Full'},
            {'id': '3', 'location': 'Library', 'fill_level': 52, 'status': 'Normal'}
        ]
    return render_template('garbage.html', bins=bins)

@app.route('/canteen')
def canteen():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    categories = {}
    db = get_db()
    if db is not None and 'food_items' in db.list_collection_names() and db.food_items.count_documents({'available': True}) > 0:
        items_cursor = db.food_items.find({"available": True})
        for item in items_cursor:
            item['id'] = str(item['_id'])
            cat = item.get('category', 'Others')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
    else:
        categories = {
            'Starters': [
                {'id': 's1', 'category': 'Starters', 'name': 'Paneer Tikka', 'price': 120.00, 'description': 'Grilled cottage cheese cubes marinated in spices'},
                {'id': 's2', 'category': 'Starters', 'name': 'Chicken 65', 'price': 150.00, 'description': 'Spicy, deep-fried chicken bites'},
            ],
            'Main Course': [
                {'id': 'm1', 'category': 'Main Course', 'name': 'Veg Biryani', 'price': 180.00, 'description': 'Aromatic rice dish cooked with mixed vegetables and spices'},
                {'id': 'm2', 'category': 'Main Course', 'name': 'Chicken Biryani', 'price': 220.00, 'description': 'Classic Hyderabadi style chicken dum biryani'},
            ],
            'Fast Food': [
                {'id': 'f1', 'category': 'Fast Food', 'name': 'Veg Burger', 'price': 60.00, 'description': 'Classic veg patty burger with cheese'},
                {'id': 'f2', 'category': 'Fast Food', 'name': 'French Fries', 'price': 50.00, 'description': 'Crispy golden potato fries'},
            ],
            'Beverages': [
                {'id': 'b1', 'category': 'Beverages', 'name': 'Cold Coffee', 'price': 60.00, 'description': 'Refreshing iced coffee with a scoop of ice cream'},
            ],
            'Desserts': [
                {'id': 'd1', 'category': 'Desserts', 'name': 'Gulab Jamun (2 pcs)', 'price': 40.00, 'description': 'Soft milk-solid dumplings soaked in sugar syrup'},
            ]
        }
    return render_template('canteen.html', categories=categories)

@app.route('/seat_reservation', methods=['GET', 'POST'])
def seat_reservation():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        venue = request.form['venue']
        seat_number = request.form['seat_number']
        res_time = request.form['reservation_time']
        
        db = get_db()
        if db is not None:
            db.seat_reservations.insert_one({
                "user_id": session['user_id'],
                "venue": venue,
                "seat_number": seat_number,
                "reservation_time": res_time,
                "created_at": datetime.now()
            })
            flash('Seat reserved successfully!', 'success')
        else:
            flash('Mock reserved!', 'success')
        return redirect(url_for('seat_reservation'))
        
    return render_template('seat_reservation.html')

@app.route('/library')
def library():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    books = []
    borrowings = []
    db = get_db()
    if db is not None and 'library_books' in db.list_collection_names() and db.library_books.count_documents({}) > 0:
        books_cursor = db.library_books.find()
        for b in books_cursor:
            b['id'] = str(b['_id'])
            books.append(b)

        borrowings_cursor = db.library_borrowings.find({"status": "Borrowed"})
        for bw in borrowings_cursor:
            bw['id'] = str(bw['_id'])
            borrowings.append(bw)
    else:
        books = [
            {'id': '1', 'title': 'Introduction to Algorithms', 'author': 'Thomas H. Cormen', 'total_copies': 5, 'available_copies': 3},
            {'id': '2', 'title': 'Clean Code', 'author': 'Robert C. Martin', 'total_copies': 3, 'available_copies': 2},
            {'id': '3', 'title': 'Computer Networks', 'author': 'Andrew S. Tanenbaum', 'total_copies': 6, 'available_copies': 4}
        ]
        borrowings = [
            {'student_name': 'student1', 'book_title': 'Introduction to Algorithms', 'borrow_date': 'Today', 'status': 'Borrowed'},
            {'student_name': 'student2', 'book_title': 'Clean Code', 'borrow_date': 'Today', 'status': 'Borrowed'},
        ]

    return render_template('library.html', books=books, borrowings=borrowings)

@app.route('/admin_panel')
def admin_panel():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('dashboard'))
    return render_template('admin_panel.html')

# IoT API Endpoint (for ESP8266 to send data)
@app.route('/api/update_sensor', methods=['POST'])
def update_sensor():
    """
    Endpoint for IoT devices (e.g., ESP8266) to POST sensor data.
    Expected JSON: {"sensor_type": "garbage", "id": "mongo_object_id_string", "value": 85}
    """
    data = request.json
    sensor_type = data.get('sensor_type')
    item_id = data.get('id')
    value = data.get('value')
    
    db = get_db()
    if db is not None:
        try:
            if sensor_type == 'garbage':
                status = 'Full' if int(value) > 90 else 'Normal'
                db.garbage_bins.update_one(
                    {'_id': ObjectId(item_id)},
                    {'$set': {'fill_level': int(value), 'status': status}}
                )
            elif sensor_type == 'irrigation':
                db.irrigation_data.update_one(
                    {'_id': ObjectId(item_id)},
                    {'$set': {'moisture_level': int(value), 'last_updated': datetime.now()}}
                )
            elif sensor_type == 'parking':
                status = 'Occupied' if int(value) == 1 else 'Free'
                db.parking_slots.update_one(
                    {'_id': ObjectId(item_id)},
                    {'$set': {'status': status}}
                )
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
            
    return jsonify({'status': 'error', 'message': 'DB connection failed'})

# --- Real-time Data Fetch Endpoints for Frontend Polling ---
@app.route('/api/data/parking')
def api_get_parking():
    simulate_sensor_data()
    db = get_db()
    if db is None: return jsonify([])
    return jsonify([{**slot, '_id': str(slot['_id'])} for slot in db.parking_slots.find()])

@app.route('/api/data/classrooms')
def api_get_classrooms():
    simulate_sensor_data()
    db = get_db()
    if db is None: return jsonify([])
    return jsonify([{**room, '_id': str(room['_id'])} for room in db.classrooms.find()])

@app.route('/api/data/irrigation')
def api_get_irrigation():
    simulate_sensor_data()
    db = get_db()
    if db is None: return jsonify([])
    data = []
    for area in db.irrigation_data.find():
        area['_id'] = str(area['_id'])
        if 'last_updated' in area:
            area['last_updated'] = str(area['last_updated'])
        data.append(area)
    return jsonify(data)

@app.route('/api/data/garbage')
def api_get_garbage():
    simulate_sensor_data()
    db = get_db()
    if db is None: return jsonify([])
    return jsonify([{**bin, '_id': str(bin['_id'])} for bin in db.garbage_bins.find()])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
