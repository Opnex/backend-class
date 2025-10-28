from database import db
from sqlalchemy import text

def add_gender_column():
    try:
        # Check if 'gender' column already exists
        check_column = text("SHOW COLUMNS FROM users LIKE 'gender';")
        result = db.execute(check_column).fetchone()
        if result:
            print("✅ 'gender' column already exists.")
            return

        # Add new column to users table
        query = text("ALTER TABLE users ADD COLUMN gender VARCHAR(10) DEFAULT 'male';")
        db.execute(query)
        db.commit()
        print("✅ 'gender' column added successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_gender_column()
