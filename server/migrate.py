import os
from sqlalchemy import create_engine
from lib.db.schema import Base
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv("DATABASE_URL")
print(db_url)
def run_migrations():
    """
    Creates all tables defined in Base metadata if they don't already exist.
    """
    try:
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        print("Database migration complete. Tables created/updated successfully.")
    except Exception as e:
        print(f"Error during database migration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Load environment variables if not already loaded (e.g., when run directly)
    # In a typical application, these would be loaded by the main entry point.
    # For standalone migration, ensure DATABASE_URL is set in the environment
    # or a .env file is loaded here.
    print(db_url)
    run_migrations()
