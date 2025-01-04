from sqlalchemy.orm import Session
from models import Credential
from schemas import CredentialCreate
from datetime import datetime

from utils import generate_signature


def create_credential(db: Session, credential: CredentialCreate):
    proof = generate_proof(credential)
    db_credential = Credential(
        context=credential.context,
        type=credential.type,
        issuer=credential.issuer,
        credentialSubject=credential.credentialSubject.dict(),
        proof=proof,
        issued_at=datetime.utcnow(),
        expiration_date=credential.expiration_date,
    )
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential

def generate_proof(credential: CredentialCreate) -> dict:
    """Genera la sección 'proof' de la credencial."""
    return {
        "type": "Ed25519Signature2018",
        "created": datetime.utcnow().isoformat() + "Z",
        "proofPurpose": "assertionMethod",
        "verificationMethod": "did:example:456#keys-1",
        "jws": generate_signature(f"{credential.issuer}-{credential.credentialSubject.id}"),
    }

def get_credential(db: Session, credential_id: int):
    return db.query(Credential).filter(Credential.id == credential_id).first()


def delete_credential(db: Session, credential_id: int):
    credential = db.query(Credential).filter(Credential.id == credential_id).first()
    if credential:
        db.delete(credential)
        db.commit()
    return credential


def revoke_credential(db: Session, credential_id: int):
    credential = db.query(Credential).filter(Credential.id == credential_id).first()
    if credential and not credential.revoked:
        credential.revoked = True
        credential.revoked_at = datetime.utcnow()
        db.commit()
        return credential
    return None
