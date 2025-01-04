from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from database import Base
from datetime import datetime

class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    context = Column(JSON, default=["https://www.w3.org/2018/credentials/v1"], nullable=False)
    type = Column(JSON, default=["VerifiableCredential"], nullable=False)
    issuer = Column(String(255), nullable=False)   # DID del emisor
    credentialSubject = Column(JSON, nullable=False)  # Información estructurada del sujeto
    proof = Column(JSON, nullable=True)  # Prueba de la credencial (firma digital)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expiration_date = Column(DateTime, nullable=True)  # Fecha de expiración opcional
