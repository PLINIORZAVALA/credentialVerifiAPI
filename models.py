"""
Define los modelos de datos utilizados en la base de datos.
Incluye la tabla de credenciales verificables.
"""

from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255), nullable=False)
    issuer = Column(String(255), nullable=False)
    claim = Column(String(255), nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    signature = Column(String(255), nullable=False)
