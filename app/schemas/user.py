from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    model_config= ConfigDict(from_attributes=True)

class UserRoleOut(BaseModel):
    id: int
    user_id : int
    organization_id : int
    role: str
    model_config = ConfigDict(from_attributes=True)
