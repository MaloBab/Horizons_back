from pydantic import BaseModel

class CategoryBase(BaseModel):
    label : str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True