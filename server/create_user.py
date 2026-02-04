# server/create_user.py
import os
import sys
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from lib.db.repository import SessionLocal
from lib.db.schema import AdminUser

# Add the server directory to the Python path

load_dotenv() # Load environment variables from .env

def create_admin_user():
    print("--- Create Admin User ---")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    db = SessionLocal()
    try:
        existing_user = db.query(AdminUser).filter_by(username=username).first()
        if existing_user:
            print(f"Error: Admin user '{username}' already exists.")
            return

        hashed_password = generate_password_hash(password)
        new_admin = AdminUser(username=username, password_hash=hashed_password)
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        print(f"Admin user '{username}' created successfully!")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
