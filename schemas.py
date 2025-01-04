from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel

class CredentialSubject(BaseModel):
    id: str  # DID del sujeto
    givenName: Optional[str]
    familyName: Optional[str]
    degree: Optional[Dict[str, str]]  # Información del título o grado

class Proof(BaseModel):
    type: str
    created: str
    proofPurpose: str
    verificationMethod: str
    jws: str

class CredentialCreate(BaseModel):
    context: Optional[List[str]] = ["https://www.w3.org/2018/credentials/v1"]
    type: Optional[List[str]] = ["VerifiableCredential"]
    issuer: str
    credentialSubject: CredentialSubject
    issued_at: Optional[str] = datetime.utcnow().isoformat() + "Z"  # Valor predeterminado
    expiration_date: Optional[str]

class CredentialResponse(CredentialCreate):
    id: int
    proof: Optional[Proof]

    class Config:
        from_attributes = True

