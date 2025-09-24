from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

from models.drug import Drug

class DrugProperty(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    drug_id: int = Field(foreign_key="drug.id")
    property_name: str
    property_value: str
    
    # Relationship - используем строку для избежания циклических импортов
    drug: Optional["Drug"] = Relationship(back_populates="properties")