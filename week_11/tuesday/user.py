from database import db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import bcrypt
import uvicorn

load_dotenv()

app = FastAPI(title="Simple App", version="1.0.0")

class Simple(BaseModel):
    name: str = Field(..., example="Sam Larry")
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")

@app.post("/signup")
def signUp(input: Simple):
    try:
        # Check for duplicate email - USING 'user' TABLE
        duplicate_query = text("""
            SELECT * FROM users  # Using 'user' table
            WHERE email = :email
        """)
        
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        # Insert new user - ALSO USING 'user' TABLE
        query = text("""
            INSERT INTO users (name, email, password)  # Changed to 'user'
            VALUES (:name, :email, :password)
        """)

        # Hash password
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)
        hashed_password_str = hashedPassword.decode('utf-8')
        print(f"Hashed password: {hashed_password_str}")
        
        db.execute(query, {
            "name": input.name, 
            "email": input.email, 
            "password": hashed_password_str
        })
        db.commit()
        
        return {
            "message": "User created successfully",
            "data": {"name": input.name, "email": input.email}
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Welcome to the API"}

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))