from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from jinja2 import Environment, FileSystemLoader

from src.db.session import get_db
from src.models.facturacion import Cliente, Factura, LineaFactura
from src.schemas.facturacion import (
    ClienteCreate, ClienteResponse,
    FacturaCreate, FacturaResponse
)

# Configurar motor de plantillas HTML
templates = Environment(loader=FileSystemLoader("src/templates"))

router = APIRouter(prefix="/facturacion", tags=["Facturación & Clientes"])

# --- CLIENTES ---
@router.post("/clientes/usuario/{usuario_id}", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(usuario_id: int, cliente: ClienteCreate, db: Session = Depends(get_db)):
    nuevo_cliente = Cliente(usuario_id=usuario_id, **cliente.model_dump())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

@router.get("/clientes/usuario/{usuario_id}", response_model=List[ClienteResponse])
def listar_clientes(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(Cliente).filter(Cliente.usuario_id == usuario_id).all()

# --- FACTURAS ---
@router.post("/facturas/usuario/{usuario_id}", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
def crear_factura(usuario_id: int, factura_in: FacturaCreate, db: Session = Depends(get_db)):
    base_imponible = Decimal("0.0")
    lineas_db = []
    
    for item in factura_in.lineas:
        subtotal = item.cantidad * item.precio_unitario
        base_imponible += subtotal
        lineas_db.append(LineaFactura(
            concepto=item.concepto,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario,
            subtotal=subtotal
        ))
    
    # Cálculo: Total = Base Imponible + IVA - IRPF
    monto_iva = base_imponible * (factura_in.porcentaje_iva / Decimal("100.0"))
    monto_irpf = base_imponible * (factura_in.porcentaje_irpf / Decimal("100.0"))
    total_factura = base_imponible + monto_iva - monto_irpf

    nueva_factura = Factura(
        usuario_id=usuario_id,
        cliente_id=factura_in.cliente_id,
        numero_factura=factura_in.numero_factura,
        fecha_emision=factura_in.fecha_emision,
        porcentaje_iva=factura_in.porcentaje_iva,
        porcentaje_irpf=factura_in.porcentaje_irpf,
        total=total_factura,
        lineas=lineas_db
    )
    
    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)
    return nueva_factura

@router.get("/facturas/usuario/{usuario_id}", response_model=List[FacturaResponse])
def listar_facturas(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(Factura).filter(Factura.usuario_id == usuario_id).all()
    
@router.get("/facturas/{factura_id}/html", response_class=HTMLResponse)
def obtener_factura_html(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    cliente = db.query(Cliente).filter(Cliente.id == factura.cliente_id).first()

    # Recalcular base para desglose de la plantilla
    base_imponible = sum(linea.subtotal for linea in factura.lineas)
    monto_iva = base_imponible * (factura.porcentaje_iva / Decimal("100.0"))
    monto_irpf = base_imponible * (factura.porcentaje_irpf / Decimal("100.0"))

    template = templates.get_template("factura.html")
    html_content = template.render(
        factura=factura,
        cliente=cliente,
        base_imponible=base_imponible,
        monto_iva=monto_iva,
        monto_irpf=monto_irpf
    )
    return HTMLResponse(content=html_content)
