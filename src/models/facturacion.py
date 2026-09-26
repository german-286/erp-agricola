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
    
    # Relación inversa con Usuario
    usuario = relationship("src.models.usuario.Usuario", back_populates="clientes")
