# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models, schemas
import bcrypt

# New imports for serving frontend
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI(title="Auth API")

# -------------------------
# CORS (IMPORTANT FOR HTML)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Serve Frontend
# -------------------------

# Mount frontend folder so script.js and style.css work
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at root URL
@app.get("/")
def serve_homepage():
    return FileResponse("frontend/index.html")


# -------------------------
# Create DB tables
# -------------------------
Base.metadata.create_all(bind=engine)

# -------------------------
# Database Session Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# REGISTER API
# -------------------------
@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Check existing email
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check existing username
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash password
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    # Create new user object
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password.decode("utf-8"),
    )

    # Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}


# -------------------------
# LOGIN API
# -------------------------
@app.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):

    # Find user by email
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Check password
    if not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user": {"id": db_user.id, "username": db_user.username}
    }
