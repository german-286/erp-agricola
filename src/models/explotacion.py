from sqlalchemy import Column, Integer, String, Numeric, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.db.session import Base

class Parcela(Base):
    __tablename__ = "parcelas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre_finca = Column(String(100), nullable=False)
    provincia = Column(String(50), nullable=True)
    municipio = Column(String(50), nullable=True)
    poligono = Column(Integer, nullable=True)
    parcela = Column(Integer, nullable=True)
    recinto = Column(Integer, nullable=True)
    referencia_catastral = Column(String(20), nullable=True, index=True)
    superficie_ha = Column(Numeric(8, 4), nullable=False)
    regimen = Column(Enum('PROPIEDAD', 'ARRENDAMIENTO', name='regimen_enum'), default='PROPIEDAD')
    coste_renta_campana = Column(Numeric(10, 2), default=0.00)

    # Relaciones
    usuario = relationship("Usuario", back_populates="parcelas")
    campana_parcelas = relationship("CampanaParcela", back_populates="parcela", cascade="all, delete-orphan")

class Campana(Base):
    __tablename__ = "campanas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)

    # Relaciones
    campana_parcelas = relationship("CampanaParcela", back_populates="campana", cascade="all, delete-orphan")

class CampanaParcela(Base):
    __tablename__ = "campana_parcela"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    campana_id = Column(Integer, ForeignKey("campanas.id"), nullable=False)
    parcela_id = Column(Integer, ForeignKey("parcelas.id"), nullable=False)
    tipo_cultivo = Column(String(50), nullable=False)
    estado_cultivo = Column(Enum('EN_PRODUCCION', 'BARBECHO', 'DESCANSO', name='estado_cultivo_enum'), default='EN_PRODUCCION')

    # Relaciones
    campana = relationship("Campana", back_populates="campana_parcelas")
    parcela = relationship("Parcela", back_populates="campana_parcelas")
    operaciones = relationship("DiarioOperaciones", back_populates="campana_parcela", cascade="all, delete-orphan")

class DiarioOperaciones(Base):
    __tablename__ = "diario_operaciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    campana_parcela_id = Column(Integer, ForeignKey("campana_parcela.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    tipo_operacion = Column(Enum('PODA', 'ARADO', 'TRATAMIENTO', 'COSECHA', 'RIEGO', 'OTRO', name='tipo_operacion_enum'), nullable=False)
    producto_aplicado = Column(String(100), nullable=True)
    coste_mano_obra = Column(Numeric(8, 2), default=0.00)

    # Relaciones
    campana_parcela = relationship("CampanaParcela", back_populates="operaciones")
