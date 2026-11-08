from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime

def setup_database():
    try:
        # Connect to local MongoDB instance
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        # Force a call to check if connection is successful
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
    except ConnectionFailure:
        print("Failed to connect to MongoDB. Please ensure MongoDB is running on localhost:27017")
        return

    db = client['smart_campus']

    # 1. Users
    if 'users' in db.list_collection_names():
        db.users.drop()
    db.users.insert_many([
        {"username": "admin", "password": "admin123", "role": "admin", "created_at": datetime.now()},
        {"username": "student1", "password": "student123", "role": "student", "created_at": datetime.now()}
    ])
    print("Users collection created and populated.")

    # 2. Parking Slots
    if 'parking_slots' in db.list_collection_names():
        db.parking_slots.drop()
    db.parking_slots.insert_many([
        {"slot_name": "P1", "status": "Free", "reserved_by": None},
        {"slot_name": "P2", "status": "Occupied", "reserved_by": None},
        {"slot_name": "P3", "status": "Free", "reserved_by": None},
        {"slot_name": "P4", "status": "Free", "reserved_by": None},
        {"slot_name": "P5", "status": "Occupied", "reserved_by": None}
    ])
    print("Parking slots collection created and populated.")

    # 3. Classrooms
    if 'classrooms' in db.list_collection_names():
        db.classrooms.drop()
    db.classrooms.insert_many([
        {"room_number": "Room 101", "usage_status": "Occupied", "lights_status": "ON", "fans_status": "ON"},
        {"room_number": "Room 102", "usage_status": "Free", "lights_status": "OFF", "fans_status": "OFF"},
        {"room_number": "Room 103", "usage_status": "Occupied", "lights_status": "ON", "fans_status": "OFF"}
    ])
    print("Classrooms collection created and populated.")

    # 4. Irrigation Data
    if 'irrigation_data' in db.list_collection_names():
        db.irrigation_data.drop()
    db.irrigation_data.insert_many([
        {"area_name": "Main Garden", "moisture_level": 45, "pump_status": "OFF", "mode": "Auto", "last_updated": datetime.now()},
        {"area_name": "Sports Field", "moisture_level": 20, "pump_status": "ON", "mode": "Auto", "last_updated": datetime.now()}
    ])
    print("Irrigation data collection created and populated.")

    # 5. Garbage Bins
    if 'garbage_bins' in db.list_collection_names():
        db.garbage_bins.drop()
    db.garbage_bins.insert_many([
        {"location": "Main Gate", "fill_level": 30, "status": "Normal"},
        {"location": "Canteen", "fill_level": 95, "status": "Full"},
        {"location": "Library", "fill_level": 50, "status": "Normal"}
    ])
    print("Garbage bins collection created and populated.")

    # 6. Food Items
    if 'food_items' in db.list_collection_names():
        db.food_items.drop()
    db.food_items.insert_many([
        {"category": "Starters", "name": "Paneer Tikka", "price": 120.00, "description": "Grilled cottage cheese cubes marinated in spices", "available": True},
        {"category": "Starters", "name": "Crispy Corn", "price": 90.00, "description": "Fried sweet corn tossed with pepper and salt", "available": True},
        {"category": "Starters", "name": "Chicken 65", "price": 150.00, "description": "Spicy, deep-fried chicken bites", "available": True},
        
        {"category": "Main Course", "name": "Veg Biryani", "price": 180.00, "description": "Aromatic rice dish cooked with mixed vegetables and spices", "available": True},
        {"category": "Main Course", "name": "Chicken Biryani", "price": 220.00, "description": "Classic Hyderabadi style chicken dum biryani", "available": True},
        {"category": "Main Course", "name": "Butter Naan & Paneer Butter Masala", "price": 200.00, "description": "Rich paneer gravy served with 2 butter naans", "available": True},
        {"category": "Main Course", "name": "Meals (Thali)", "price": 150.00, "description": "Traditional South Indian full meal", "available": True},

        {"category": "Fast Food", "name": "Veg Burger", "price": 60.00, "description": "Classic veg patty burger with cheese", "available": True},
        {"category": "Fast Food", "name": "Chicken Burger", "price": 90.00, "description": "Crispy chicken patty with fresh lettuce", "available": True},
        {"category": "Fast Food", "name": "French Fries", "price": 50.00, "description": "Crispy golden potato fries", "available": True},
        
        {"category": "Beverages", "name": "Cold Coffee", "price": 60.00, "description": "Refreshing iced coffee with a scoop of ice cream", "available": True},
        {"category": "Beverages", "name": "Mango Lassi", "price": 50.00, "description": "Sweet yogurt drink blended with fresh mango pulp", "available": True},
        {"category": "Beverages", "name": "Fresh Lime Soda", "price": 40.00, "description": "Chilled sweet and salt lime soda", "available": True},
        
        {"category": "Desserts", "name": "Gulab Jamun (2 pcs)", "price": 40.00, "description": "Soft milk-solid dumplings soaked in sugar syrup", "available": True},
        {"category": "Desserts", "name": "Chocolate Brownie with Ice Cream", "price": 100.00, "description": "Warm brownie topped with vanilla ice cream", "available": True}
    ])
    print("Food items collection created and populated.")
    
    # Empty collections for orders and reservations
    if 'orders' in db.list_collection_names():
        db.orders.drop()
    db.create_collection('orders')
    
    if 'seat_reservations' in db.list_collection_names():
        db.seat_reservations.drop()
    db.create_collection('seat_reservations')

    # 7. Library Module
    if 'library_books' in db.list_collection_names():
        db.library_books.drop()
    db.library_books.insert_many([
        {"title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "total_copies": 5, "available_copies": 3},
        {"title": "Clean Code", "author": "Robert C. Martin", "total_copies": 3, "available_copies": 3},
        {"title": "Design Patterns", "author": "Erich Gamma", "total_copies": 4, "available_copies": 0},
        {"title": "Computer Networks", "author": "Andrew S. Tanenbaum", "total_copies": 6, "available_copies": 5}
    ])
    print("Library books collection created and populated.")

    if 'library_borrowings' in db.list_collection_names():
        db.library_borrowings.drop()
    db.library_borrowings.insert_many([
        {"student_name": "student1", "book_title": "Introduction to Algorithms", "borrow_date": datetime.now(), "status": "Borrowed"},
        {"student_name": "student2", "book_title": "Introduction to Algorithms", "borrow_date": datetime.now(), "status": "Borrowed"},
        {"student_name": "student1", "book_title": "Design Patterns", "borrow_date": datetime.now(), "status": "Borrowed"},
        {"student_name": "student3", "book_title": "Computer Networks", "borrow_date": datetime.now(), "status": "Borrowed"}
    ])
    print("Library borrowings collection created and populated.")

    print("\nDatabase setup complete! You can now run the Flask application.")

if __name__ == "__main__":
    setup_database()
