"""
Define los modelos de datos utilizados en la base de datos.
Incluye la tabla de credenciales verificables.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from database import Base
from datetime import datetime

class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    context = Column(JSON, default=["https://www.w3.org/2018/credentials/v1"], nullable=False)
    type = Column(JSON, default=["VerifiableCredential"], nullable=False)
    subject = Column(String(255), nullable=False)  # DID del sujeto
    issuer = Column(String(255), nullable=False)   # DID del emisor
    claim = Column(JSON, nullable=False)  # Información estructurada
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expiration_date = Column(DateTime, nullable=True)  # Fecha de expiración opcional
    revoked = Column(Boolean, default=False, nullable=False)  # Indica si fue revocada
    revoked_at = Column(DateTime, nullable=True)  # Fecha de revocación
    signature = Column(String(512), nullable=False)  # Firma digital
