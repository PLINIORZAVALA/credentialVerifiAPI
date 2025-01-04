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
        credentialSubject=credential.credentialSubject or {},
        claim=credential.claim or {},  # Asigna un diccionario vacío si está ausente
        proof=proof or {},
        issuanceDate=datetime.utcnow(),
        expirationDate=None,
        signature=credential.signature or generate_signature(
            f"{credential.issuer}-{credential.credentialSubject.get('id', 'unknown')}"
        ),
        revoked=False,
        revoked_at=None,
    )

    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential


def generate_proof(credential: CredentialCreate):
    return {
        "type": "Ed25519Signature2020",
        "created": datetime.utcnow().isoformat(),
        "proofPurpose": "assertionMethod",
        "verificationMethod": f"{credential.issuer}#keys-1",
        "jws": generate_signature(f"{credential.issuer}-{credential.credentialSubject['id']}"),
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
