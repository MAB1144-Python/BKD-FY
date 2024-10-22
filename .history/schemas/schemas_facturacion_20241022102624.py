from pydantic import BaseModel

class FacturaCreate(BaseModel):
    cliente_id: int
    productos: list[int]
    total: float

class FacturaResponse(BaseModel):
    id: int
    cliente_id: int
    productos: list[int]
    total: float