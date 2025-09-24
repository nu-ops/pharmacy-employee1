from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Drug(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    atc_code: Optional[str] = None
    description: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    quantity: int
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships - используем строки для избежания циклических импортов
    properties: List["DrugProperty"] = Relationship(back_populates="drug")
    sales: List["Sale"] = Relationship(back_populates="drug")
    
    def __repr__(self):
        return f"Drug(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity})"