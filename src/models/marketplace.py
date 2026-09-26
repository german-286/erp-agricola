from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from src.db.session import Base
import enum

class CategoriaServicio(str, enum.Enum):
    MAQUINARIA = "MAQUINARIA"
    TALA = "TALA"
    TRATAMIENTO = "TRATAMIENTO"
    COSECHA = "COSECHA"
    RIEGO = "RIEGO"
    OTROS = "OTROS"

class MarketplaceServicio(Base):
    __tablename__ = "marketplace_servicios"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    empresa_nombre = Column(String(150), nullable=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria = Column(Enum(CategoriaServicio), nullable=False, default=CategoriaServicio.OTROS)
    precio_estimado = Column(Numeric(10, 2), nullable=True)
    unidad_precio = Column(String(50), nullable=True)
    provincia = Column(String(100), nullable=True)
    telefono = Column(String(20), nullable=True)
    es_patrocinado = Column(Boolean, default=False)

    usuario = relationship("src.models.usuario.Usuario")
