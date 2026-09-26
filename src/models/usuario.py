from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.session import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    nif_cif = Column(String(20), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    direccion_fiscal = Column(String(200), nullable=True)
    iban = Column(String(34), nullable=True)

    # Restablecemos las propiedades de las relaciones que necesitan los otros mappers
    parcelas = relationship("Parcela", back_populates="usuario", cascade="all, delete-orphan")
    clientes = relationship("Cliente", back_populates="usuario", cascade="all, delete-orphan")

