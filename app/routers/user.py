from fastapi import APIRouter, Depends, HTTPException, Query, Security, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.crud import user as user_crud
from app.database import SessionLocal
from typing import List, Dict
from app.security.jwt import create_access_token, get_current_user, create_password_reset_token, verify_token
from app.email.config import send_email
from app.email.templates import get_password_reset_email
import os

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=user_schema.UserResponse)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email=user.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@router.post("/login", response_model=user_schema.Token)
def login(user_credentials: user_schema.UserLogin, db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(db, email=user_credentials.email, password=user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=user_schema.UserResponse)
def read_users_me(
    current_user: dict = Security(get_current_user),
    db: Session = Depends(get_db)
):
    user = user_crud.get_user_by_email(db, email=current_user["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Authenticated password reset (when user knows their password)
@router.put("/reset_password", response_model=Dict[str, str])
def reset_password(
    email: str = Query(...),
    new_password: str = Query(...),
    current_user: dict = Security(get_current_user),
    db: Session = Depends(get_db)
):
    if email != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Not authorized to reset this user's password")
    
    user = user_crud.reset_password(db, email, new_password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password updated successfully"}

# Request password reset (when user forgot password)
@router.post("/forgot-password", response_model=Dict[str, str])
async def forgot_password(
    request: user_schema.PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user = user_crud.get_user_by_email(db, email=request.email)
    if not user:
        return {"message": "If the email exists, a password reset link will be sent"}
    
    reset_token = create_password_reset_token(request.email)
    
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    email_content = get_password_reset_email(request.email, reset_token, frontend_url)
    
    background_tasks.add_task(
        send_email,
        to_email=request.email,
        subject=email_content["subject"],
        body=email_content["body"]
    )
    
    return {"message": "If the email exists, password reset instructions will be sent"}

# Reset password using token (when user forgot password)
@router.post("/reset-password-with-token", response_model=Dict[str, str])
def reset_password_with_token(reset_data: user_schema.PasswordReset, db: Session = Depends(get_db)):
    try:
        payload = verify_token(reset_data.token, token_type="reset")
        email = payload["sub"]
        
        user = user_crud.reset_password(db, email, reset_data.new_password)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"message": "Password has been reset successfully"}
    except HTTPException as e:
        if e.status_code == 401:
            raise HTTPException(
                status_code=400,
                detail="Invalid or expired reset token"
            )
        raise
