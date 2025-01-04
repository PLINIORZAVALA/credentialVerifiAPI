"""
Define los esquemas de validación para solicitudes y respuestas.
"""

from pydantic import BaseModel
from datetime import datetime

class CredentialCreate(BaseModel):
    subject: str
    issuer: str
    claim: str

class CredentialResponse(BaseModel):
    id: int
    subject: str
    issuer: str
    claim: str
    issued_at: datetime
    signature: str

    class Config:
        from_attributes = True  # Actualizado para Pydantic V2

"""
Lógica de negocio para la gestión de credenciales verificables.
"""
from sqlalchemy.orm import Session
from models import Credential
from schemas import CredentialCreate
from utils import generate_signature
from datetime import datetime

def create_credential(db: Session, credential: CredentialCreate):
    db_credential = Credential(
        subject=credential.subject,
        issuer=credential.issuer,
        claim=credential.claim,
        signature=generate_signature(f"{credential.subject}-{credential.claim}"),  # Generar firma
        issued_at=datetime.utcnow(),  # Inicializar issued_at
    )
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential

def get_credential(db: Session, credential_id: int):
    return db.query(Credential).filter(Credential.id == credential_id).first()

def delete_credential(db: Session, credential_id: int):
    credential = db.query(Credential).filter(Credential.id == credential_id).first()
    if credential:
        db.delete(credential)
        db.commit()
    return credential
