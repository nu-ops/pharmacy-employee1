from sqlmodel import SQLModel, Field
from typing import Optional

class Supplier(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
    def __repr__(self):
        return f"Supplier(id={self.id}, name='{self.name}')"