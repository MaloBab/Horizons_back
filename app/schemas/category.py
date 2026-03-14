from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    label: str
    responsible: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)