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
    context: List[str] = ["https://www.w3.org/2018/credentials/v1"]
    type: List[str] = ["VerifiableCredential"]
    issuer: str
    credentialSubject: Dict[str, str]  # Definido como un diccionario
    claim: Dict[str, str]
    signature: Optional[str] = None


class CredentialResponse(BaseModel):
    id: int
    context: List[str]
    type: List[str]
    subject: Optional[str]  # Derivado de credentialSubject["id"]
    issuer: str
    claim: Optional[Dict[str, str]]  # claim puede ser null
    issued_at: datetime
    expiration_date: Optional[datetime]
    revoked: bool
    revoked_at: Optional[datetime]
    signature: Optional[str]  # signature puede ser null

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            context=obj.context,
            type=obj.type,
            subject=obj.credentialSubject.get("id") if obj.credentialSubject else None,
            issuer=obj.issuer,
            claim=obj.claim if obj.claim else {},
            issued_at=obj.issued_at,
            expiration_date=obj.expiration_date,
            revoked=obj.revoked,
            revoked_at=obj.revoked_at,
            signature=obj.signature,
        )

