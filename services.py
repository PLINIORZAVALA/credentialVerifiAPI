from sqlalchemy.orm import Session
from models import Credential
from schemas import CredentialCreate
from datetime import datetime

from utils import generate_signature


def create_credential(db: Session, credential: CredentialCreate):
    db_credential = Credential(
        context=["https://www.w3.org/2018/credentials/v1"],  # Valor por defecto
        type=["VerifiableCredential"],                      # Valor por defecto
        subject=credential.subject,
        issuer=credential.issuer,
        claim=credential.claim,
        signature=credential.signature or generate_signature(f"{credential.subject}-{credential.claim}"),
        issued_at=datetime.utcnow(),
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


def revoke_credential(db: Session, credential_id: int):
    credential = db.query(Credential).filter(Credential.id == credential_id).first()
    if credential and not credential.revoked:
        credential.revoked = True
        credential.revoked_at = datetime.utcnow()
        db.commit()
        return credential
    return None
