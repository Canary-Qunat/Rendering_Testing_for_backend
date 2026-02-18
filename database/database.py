from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, Token
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, time

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_token_to_db(access_token: str, db: Session):
    # Delete ALL old tokens before saving new one (Single user sys)
    db.query(Token).delete()
    db.commit()
    """
    Saves a token and calculates expiration to be exactly 6:00 AM 
    on the day following the current timestamp.
    """
    # 1. Get current UTC time
    now = datetime.utcnow()
    
    # 2. Calculate the date for tomorrow
    tomorrow_date = (now + timedelta(days=1)).date()
    
    # 3. Create a datetime object for tomorrow at 06:00:00
    expiry_date = datetime.combine(tomorrow_date, time(6, 0, 0))
    
    token = Token(access_token=access_token, expired_at=expiry_date)
    db.add(token)
    db.commit()
    db.refresh(token)

    print(f" Token saved to database: ID={token.id}, expired at {expiry_date}")

    return token

def get_latest_token(db: Session):
    """
    Retrieves the most recent VALID token from the database.
    This is for single-user use - returns ANY valid token found.
    
    Returns the access_token string if found, None otherwise.
    """
    print(f" Checking database for valid tokens (expired_at > {datetime.utcnow()})")
    
    token = db.query(Token).filter(
        Token.expired_at > datetime.utcnow()
    ).order_by(
        Token.created_at.desc()
    ).first()
    
    if token:
        print(f"Found valid token: ID={token.id}, Created={token.created_at}, expired={token.expired_at}")
        return token.access_token
    else:
        print(f"No valid token found in database")
        return None

def check_token_validity(db: Session):
    """
    Check if there's ANY valid token in the database.
    Returns True if valid token exists, False otherwise.
    """
    token = get_latest_token(db)
    return token is not None

def delete_expired_tokens(db: Session):
    """
    Delete all expired tokens from the database.
    Useful for cleanup.
    """
    deleted_count = db.query(Token).filter(
        Token.expired_at <= datetime.utcnow()
    ).delete()
    db.commit()
    print(f" Deleted {deleted_count} expired tokens")
    return deleted_count

def get_token_info(db: Session):
    """
    Get information about the latest token for debugging.
    """
    token = db.query(Token).order_by(Token.created_at.desc()).first()
    
    if not token:
        return {
            "exists": False,
            "message": "No tokens in database"
        }
    
    now = datetime.utcnow()
    is_valid = token.expired_at > now
    time_remaining = token.expired_at - now if is_valid else timedelta(0)
    
    return {
        "exists": True,
        "is_valid": is_valid,
        "created_at": token.created_at.isoformat(),
        "expired_at": token.expired_at.isoformat(),
        "time_remaining": str(time_remaining) if is_valid else "Expired",
        "token_preview": token.access_token[:10] + "..."

    }
