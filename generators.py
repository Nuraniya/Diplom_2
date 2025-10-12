import random

def generate_email():
    return f"test{random.randint(10000, 99999)}@test.com"

def generate_user_data():
    return {
        "email": generate_email(),
        "password": "password123",
        "name": "Test User"
    }