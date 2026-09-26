from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.db.session import Base

class Cliente(Base):
    __tablename__ = "clientes"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nif_cif = Column(String(20), nullable=False)
    nombre_empresa = Column(String(150), nullable=False)
    direccion = Column(String(255), nullable=True)
    telefono = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

    usuario = relationship("src.models.usuario.Usuario", back_populates="clientes")
    facturas = relationship("Factura", back_populates="cliente")


class Factura(Base):
    __tablename__ = "facturas"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    numero_factura = Column(String(50), nullable=False, unique=True)
    fecha_emision = Column(Date, nullable=False)
    porcentaje_iva = Column(Numeric(5, 2), default=21.0)
    porcentaje_irpf = Column(Numeric(5, 2), default=0.0)
    total = Column(Numeric(10, 2), default=0.0)

    cliente = relationship("Cliente", back_populates="facturas")
    lineas = relationship("LineaFactura", back_populates="factura", cascade="all, delete-orphan")


class LineaFactura(Base):
    __tablename__ = "lineas_factura"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    concepto = Column(String(255), nullable=False)
    cantidad = Column(Numeric(10, 2), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    factura = relationship("Factura", back_populates="lineas")
