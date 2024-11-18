from pydantic import BaseModel
from datetime import datetime

class MessageRequest(BaseModel):
    sender_id: int
    receiver_id: int
    content: str