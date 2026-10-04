from fastapi import APIRouter, Depends
from ..schemas.user import UserResponse
from ..core.dependencies import get_current_user
from ..models.user import Users

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: Users = Depends(get_current_user)):
    """
    Получение информации о текущем пользователе
    Эндпоинт защищен: требудется валидный access токен
    """
    
    return current_user
    