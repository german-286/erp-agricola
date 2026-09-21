from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from src.db.session import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    nif_cif = Column(String(20), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    direccion_fiscal = Column(String(200), nullable=True)
    iban = Column(String(34), nullable=True)

    # Relaciones
    clientes = relationship("Cliente", back_populates="usuario", cascade="all, delete-orphan")
    parcelas = relationship("Parcela", back_populates="usuario", cascade="all, delete-orphan")
    facturas = relationship("Factura", back_populates="usuario", cascade="all, delete-orphan")


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nif_cif = Column(String(20), nullable=False, index=True)
    nombre_empresa = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=True)
    telefono = Column(String(20), nullable=True)

    # Relaciones
    usuario = relationship("Usuario", back_populates="clientes")
    facturas = relationship("Factura", back_populates="cliente")
