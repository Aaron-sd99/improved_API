from pydantic import BaseModel, ConfigDict
from typing import Optional

class OrganizationCreate(BaseModel):
    name : str
    billing_email: Optional[str] = None
    locale : Optional[str]="es"
    timezone : Optional[str]="UTC"

class OrganizationOut(OrganizationCreate):
    id: int
    model_config =ConfigDict(from_attributes=True)

class OrgUserAssign(BaseModel):
    user_id: int
    role: str

    