from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 
from jose import JWTError 
from ..database.db import get_db
from ..models.user import Users
from ..schemas.token import TokenData
from .security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Users:
    """
    Зависимость, которая извлекает текущего пользователя из токена.
    Используется для защиты эндпоинтов
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WW-Authenticate":"Bearer"}
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    token_data = TokenData(user_id=int(user_id))
    
    user = db.query(Users).filter(Users.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    
    return user 

    