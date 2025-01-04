from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel

class CredentialSubject(BaseModel):
    id: str
    givenName: Optional[str]
    familyName: Optional[str]
    degree: Optional[Dict[str, str]]

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
    claim: Optional[Dict[str, str]] = None  # Asegúrate de que este campo exista
    signature: Optional[str] = None


class CredentialResponse(BaseModel):
    id: int
    context: List[str]
    type: List[str]
    credentialSubject: Dict[str, str]
    issuer: str
    issuanceDate: datetime
    expirationDate: Optional[datetime]
    proof: Proof
    revoked: bool
    revoked_at: Optional[datetime]
    signature: Optional[str]

    class Config:
        orm_mode = True
