from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base
from schemas import CredentialCreate, CredentialResponse
from services import create_credential, get_credential, delete_credential, revoke_credential
from utils import generate_signature

app = FastAPI()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Credenciales Verificables"}


@app.post("/credentials/", response_model=CredentialResponse)
def create_new_credential(credential: CredentialCreate, db: Session = Depends(get_db)):
    credential.signature = generate_signature(f"{credential.issuer}-{credential.credentialSubject['id']}")
    created_credential = create_credential(db, credential)
    return CredentialResponse.from_orm(created_credential)


@app.get("/credentials/{credential_id}", response_model=CredentialResponse)
def read_credential(credential_id: int, db: Session = Depends(get_db)):
    credential = get_credential(db, credential_id)
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")
    return CredentialResponse.from_orm(credential)


@app.post("/credentials/{credential_id}/revoke")
def revoke_existing_credential(credential_id: int, db: Session = Depends(get_db)):
    credential = revoke_credential(db, credential_id)
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")
    return {"message": f"Credential {credential_id} revoked successfully"}


@app.delete("/credentials/{credential_id}")
def delete_existing_credential(credential_id: int, db: Session = Depends(get_db)):
    credential = delete_credential(db, credential_id)
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")
    return {"message": f"Credential {credential_id} deleted successfully"}
