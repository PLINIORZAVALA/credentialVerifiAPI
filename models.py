from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from database import Base
from datetime import datetime

class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    context = Column(JSON, default=["https://www.w3.org/2018/credentials/v1"], nullable=False)
    type = Column(JSON, default=["VerifiableCredential"], nullable=False)
    issuer = Column(String(255), nullable=False)
    credentialSubject = Column(JSON, nullable=False)  # Campo JSON para almacenar el objeto
    claim = Column(JSON, nullable=False)
    proof = Column(JSON, nullable=True)  # Campo para almacenar el proof
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expiration_date = Column(DateTime, nullable=True)  # Campo opcional para la fecha de expiración
    signature = Column(String(512), nullable=True)
    revoked = Column(Boolean, default=False, nullable=False)
    revoked_at = Column(DateTime, nullable=True)
