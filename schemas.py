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
    issuer: str
    claim: str
    issued_at: datetime
    signature: str

    class Config:
        orm_mode = True
