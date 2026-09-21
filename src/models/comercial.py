from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.db.session import Base

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    numero_factura = Column(String(50), nullable=False, unique=True, index=True)
    fecha_emision = Column(Date, nullable=False)
    porcentaje_iva = Column(Numeric(5, 2), default=21.00)
    porcentaje_irpf = Column(Numeric(5, 2), default=2.00)
    total = Column(Numeric(10, 2), nullable=False, default=0.00)

    # Relaciones
    usuario = relationship("Usuario", back_populates="facturas")
    cliente = relationship("Cliente", back_populates="facturas")
    lineas = relationship("LineaFactura", back_populates="factura", cascade="all, delete-orphan")


class LineaFactura(Base):
    __tablename__ = "lineas_factura"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    concepto = Column(String(200), nullable=False)
    cantidad = Column(Numeric(8, 2), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    # Relaciones
    factura = relationship("Factura", back_populates="lineas")


class MarketplaceServicios(Base):
    __tablename__ = "marketplace_servicios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_nombre = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    provincia = Column(String(50), nullable=False)
    es_patrocinado = Column(Boolean, default=False)
