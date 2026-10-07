from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: str 
    name: str 

class UserResponse(BaseModel):
    id: int 
    email: EmailStr
    name: str 
    
    model_config = ConfigDict(from_attributes=True)
