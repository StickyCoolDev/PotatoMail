# server/lib/auth/utils.py
from werkzeug.security import generate_password_hash
from lib.db.repository import SessionLocal
from lib.db.schema import AdminUser

def create_initial_admin_user(username, password):
    db = SessionLocal()
    existing_user = db.query(AdminUser).filter_by(username=username).first()
    if not existing_user:
        hashed_password = generate_password_hash(password)
        new_admin = AdminUser(username=username, password_hash=hashed_password)
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        print(f"Initial admin user '{username}' created.")
    else:
        print(f"Admin user '{username}' already exists.")
    db.close()
