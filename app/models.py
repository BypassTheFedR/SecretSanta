from pydantic import BaseModel, EmailStr
from typing import List, Optional

class FamilyParticipant(BaseModel):
    name: str
    email: EmailStr
    spouse_name: Optional[str] = None
    spouse_email: Optional[EmailStr] = None
    children: Optional[List[str]] = None
    

