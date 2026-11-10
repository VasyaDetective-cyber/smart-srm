import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.models.models import User
from src.core.auth import get_password_hash

load_dotenv()

def create_initial_admin():
    db: Session = SessionLocal()
    try:
        admin_email = os.getenv("ADMIN_EMAIL", "admin@crm.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "SuperSecureAdminPassword123!")
        admin_name = os.getenv("ADMIN_NAME", "System Administrator")

        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if existing_admin:
            print(f"Admin with email {admin_email} already exists.")
            return

        admin_user = User(
            email=admin_email,
            password_hash=get_password_hash(admin_password),
            full_name=admin_name,
            role="Admin"
        )
        db.add(admin_user)
        db.commit()
        print(f"Initial admin created successfully: {admin_email}")
    except Exception as e:
        db.rollback()
        print(f"Error creating admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()