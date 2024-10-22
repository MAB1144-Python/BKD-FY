from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
#from models import Factura, Producto, Cliente
from schemas.schemas_facturacion import FacturaCreate, FacturaResponse, Factura, Producto, Cliente
from utils.sesion_database import get_db



router = APIRouter()

db=get_db()

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


