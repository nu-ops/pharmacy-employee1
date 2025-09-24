from sqlmodel import SQLModel, Field
from typing import Optional

class Pharmacy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    address: str
    city: str
    phone: Optional[str] = None
    
    def __repr__(self):
        return f"Pharmacy(id={self.id}, address='{self.address}', city='{self.city}')"