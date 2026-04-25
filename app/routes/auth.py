from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..database import get_db
from app.utils import utils
from app.models.users import Users
from app.oauth2 import create_acces_token

router = APIRouter(tags="Auth")

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credential")
    
    if not utils.verify(form_data.password, user.password):
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid credentials"
    )
    acces_token = create_acces_token(data={"user_id": user.id})

    return {"access_token": acces_token, "token_type": "bearer"}