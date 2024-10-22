from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Factura, Producto, Cliente
from schemas.schemas_facturacion import FacturaCreate, FacturaResponse
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/facturas/", response_model=FacturaResponse)
def create_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
    db_factura = Factura(cliente_id=factura.cliente_id, total=factura.total)
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    for producto_id in factura.productos:
        producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        db_factura.productos.append(producto)
    db.commit()
    return db_factura

@router.get("/facturas/{factura_id}", response_model=FacturaResponse)
def read_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

@router.get("/facturas/", response_model=list[FacturaResponse])
def read_facturas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    facturas = db.query(Factura).offset(skip).limit(limit).all()
    return facturas

@router.delete("/facturas/{factura_id}", response_model=FacturaResponse)
def delete_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    db.delete(factura)
    db.commit()
    return factura
    factura_producto = Table(
        'factura_producto',
        Base.metadata,
        Column('factura_id', Integer, ForeignKey('facturas.id'), primary_key=True),
        Column('producto_id', Integer, ForeignKey('productos.id'), primary_key=True)
    )

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



