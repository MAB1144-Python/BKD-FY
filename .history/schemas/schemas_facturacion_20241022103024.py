from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table

class FacturaCreate(BaseModel):
    cliente_id: int
    productos: list[int]
    total: float

class FacturaResponse(BaseModel):
    id: int
    cliente_id: int
    productos: list[int]
    total: float
    
class Factura(Base):
    __tablename__ = 'facturas'

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    total = Column(Float)
    productos = relationship('Producto', secondary=factura_producto, back_populates='facturas')
    cliente = relationship('Cliente', back_populates='facturas')

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    facturas = relationship('Factura', secondary=factura_producto, back_populates='productos')

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    facturas = relationship('Factura', back_populates='cliente')
