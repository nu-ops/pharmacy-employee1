from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Sale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    drug_id: int = Field(foreign_key="drug.id")
    quantity: int
    sale_price: float
    sale_date: datetime = Field(default_factory=datetime.now)
    
    # Relationship - используем строку для избежания циклических импортов
    drug: Optional["Drug"] = Relationship(back_populates="sales") # type: ignore
    
    def __repr__(self):
        return f"Sale(id={self.id}, drug_id={self.drug_id}, quantity={self.quantity})"