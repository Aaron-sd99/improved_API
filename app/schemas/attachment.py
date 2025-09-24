from pydantic import BaseModel, ConfigDict

class AttachmentOut(BaseModel):
    id: int
    post_id: int
    filename: str
    mime: str
    size: int
    model_config=ConfigDict(from_attributes=True)

