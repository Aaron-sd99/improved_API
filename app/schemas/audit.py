from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AuditOut(BaseModel):
    id: int
    actor_id: int
    action: str
    entity: str
    entity_id: int
    before: Optional[str] =None
    after: Optional[str]= None
    at: datetime
    model_config= ConfigDict(from_attributes=True)

