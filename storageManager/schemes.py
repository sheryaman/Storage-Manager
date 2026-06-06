from pydantic import BaseModel, Field

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: str
    
    model_config = {"from_attributes": True}

class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0, description="The number must be greater than zero")
    stock: int = Field(ge=0, description="The number must be greater or equal to zero")
    category_name: str

class CategoryCreate(BaseModel):
    name: str

class StockUpdate(BaseModel):
    new_stock: int
