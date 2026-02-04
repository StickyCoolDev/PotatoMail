import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.schema import Email, Base

# Database connection setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@host:port/dbname")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_new_email(to_email: str, subject: str, body: str, html_body: str | None = None):
    try:
        db = SessionLocal()
        new_email = Email(
            Subject=subject,
            Body=body,
            ReceiverEmail=to_email,
            HtmlBody=html_body
        )
        db.add(new_email)
        db.commit()
        db.refresh(new_email)
        print("Email row added successfully:", new_email)
        return new_email
    except Exception as e:
        db.rollback()
        print("Error adding email row:", e)
        raise
    finally:
        db.close()