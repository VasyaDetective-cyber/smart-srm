import os
import sys
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.models.models import User
from src.core.auth import get_password_hash

load_dotenv()

def create_initial_admin():
    db: Session = SessionLocal()
    try:
        admin_email = os.environ["ADMIN_EMAIL"].strip().lower()
        admin_password = os.environ["ADMIN_PASSWORD"]
        admin_name = os.environ.get("ADMIN_NAME", "System Administrator").strip()

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
    except KeyError as e:
        db.rollback()
        print(f"Missing required environment variable for admin creation: {e}")
        sys.exit(1)
    except Exception as e:
        db.rollback()
        print(f"Error creating admin: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()