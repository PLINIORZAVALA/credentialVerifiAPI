"""
API para gestionar credenciales verificables.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, Credential
from schemas import CredentialCreate, CredentialResponse
from services import create_credential, get_credential, delete_credential, revoke_credential
from utils import generate_signature

# Inicializar la aplicación FastAPI
app = FastAPI()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Root"])
def read_root():
    """Devuelve un mensaje de bienvenida a la API."""
    return {"message": "Bienvenido a la API de Credenciales Verificables"}


@app.post("/credentials/", response_model=CredentialResponse)
def create_new_credential(credential: CredentialCreate, db: Session = Depends(get_db)):
    """Crea una nueva credencial verificable."""
    existing_credential = db.query(Credential).filter(
        Credential.subject == credential.subject,
        Credential.issuer == credential.issuer,
        Credential.claim == credential.claim,
    ).first()
    if existing_credential:
        raise HTTPException(status_code=400, detail="Credential already exists")

    credential.signature = generate_signature(f"{credential.subject}-{credential.claim}")
    return create_credential(db, credential)


@app.get("/credentials/{credential_id}", response_model=CredentialResponse, tags=["Credentials"])
def read_credential(credential_id: int, db: Session = Depends(get_db)):
    """Obtiene una credencial específica por su ID."""
    credential = get_credential(db, credential_id)
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")
    return credential


@app.post("/credentials/{credential_id}/revoke", tags=["Credentials"])
def revoke_existing_credential(credential_id: int, db: Session = Depends(get_db)):
    """Revoca una credencial específica."""
    credential = revoke_credential(db, credential_id)
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")
    return {"message": f"Credential {credential_id} revoked successfully"}


@app.get("/credentials/", tags=["Credentials"])
def search_credentials(
    subject: str = Query(None, description="DID del sujeto"),
    issuer: str = Query(None, description="DID del emisor"),
    claim: str = Query(None, description="Descripción del reclamo"),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de registros a devolver"),
    db: Session = Depends(get_db),
):
    """Busca credenciales por filtros específicos con paginación."""
    query = db.query(Credential)
    if subject:
        query = query.filter(Credential.subject == subject)
    if issuer:
        query = query.filter(Credential.issuer == issuer)
    if claim:
        query = query.filter(Credential.claim == claim)

    results = query.offset(skip).limit(limit).all()
    if not results:
        raise HTTPException(status_code=404, detail="No credentials found")
    return results


@app.delete("/credentials/{credential_id}", tags=["Credentials"])
def delete_existing_credential(credential_id: int, db: Session = Depends(get_db)):
    """Elimina una credencial específica por su ID."""
    credential = delete_credential(db, credential_id)
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")
    return {"message": f"Credential {credential_id} deleted successfully"}
