from pydantic import BaseModel, ConfigDict

class BlogCreate(BaseModel):
    name: str

class BlogOut(BlogCreate):
    id: int
    organization_id : int
    model_config= ConfigDict(from_attributes=True)

