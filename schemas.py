"""
Define los esquemas de validación para solicitudes y respuestas.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class CredentialCreate(BaseModel):
    context: Optional[List[str]] = ["https://www.w3.org/2018/credentials/v1"]
    type: Optional[List[str]] = ["VerifiableCredential"]
    subject: str
    issuer: str
    claim: str
    signature: Optional[str] = None

class CredentialResponse(BaseModel):
    id: int
    subject: str
    issuer: str
    claim: str
    issued_at: datetime
    signature: str
    revoked: bool
    revoked_at: Optional[datetime]

    class Config:
        orm_mode = True
