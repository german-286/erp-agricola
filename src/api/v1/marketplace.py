from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from src.db.session import get_db
from src.models.marketplace import MarketplaceServicio
from src.schemas.marketplace import MarketplaceServicioCreate, MarketplaceServicioResponse

router = APIRouter(prefix="/marketplace", tags=["Marketplace de Servicios"])

@router.post("/servicios/usuario/{usuario_id}", response_model=MarketplaceServicioResponse, status_code=status.HTTP_201_CREATED)
def publicar_servicio(usuario_id: int, servicio: MarketplaceServicioCreate, db: Session = Depends(get_db)):
    nuevo_servicio = MarketplaceServicio(usuario_id=usuario_id, **servicio.model_dump())
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio

@router.get("/servicios", response_model=List[MarketplaceServicioResponse])
def listar_servicios(categoria: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(MarketplaceServicio)
    if categoria:
        query = query.filter(MarketplaceServicio.categoria == categoria)
    return query.all()

@router.get("/servicios/usuario/{usuario_id}", response_model=List[MarketplaceServicioResponse])
def listar_servicios_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(MarketplaceServicio).filter(MarketplaceServicio.usuario_id == usuario_id).all()
