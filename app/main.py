from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inscrições API",
    version="1.0.0",
    description="API secundária para gerenciamento de inscrições em eventos.",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post(
    "/inscricoes",
    response_model=schemas.InscricaoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_inscricao(
    inscricao: schemas.InscricaoCreate,
    db: Session = Depends(get_db),
):
    nova_inscricao = models.Inscricao(**inscricao.model_dump())
    db.add(nova_inscricao)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Este e-mail já está inscrito neste evento",
        )

    db.refresh(nova_inscricao)
    return nova_inscricao


@app.get("/inscricoes", response_model=list[schemas.InscricaoResponse])
def listar_inscricoes(db: Session = Depends(get_db)):
    return db.query(models.Inscricao).order_by(models.Inscricao.id).all()


@app.get(
    "/inscricoes/evento/{evento_id}",
    response_model=list[schemas.InscricaoResponse],
)
def listar_por_evento(evento_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Inscricao)
        .filter(models.Inscricao.evento_id == evento_id)
        .order_by(models.Inscricao.nome)
        .all()
    )


@app.get("/inscricoes/{inscricao_id}", response_model=schemas.InscricaoResponse)
def buscar_inscricao(inscricao_id: int, db: Session = Depends(get_db)):
    inscricao = (
        db.query(models.Inscricao)
        .filter(models.Inscricao.id == inscricao_id)
        .first()
    )

    if not inscricao:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")

    return inscricao


@app.put("/inscricoes/{inscricao_id}", response_model=schemas.InscricaoResponse)
def atualizar_inscricao(
    inscricao_id: int,
    dados: schemas.InscricaoUpdate,
    db: Session = Depends(get_db),
):
    inscricao = (
        db.query(models.Inscricao)
        .filter(models.Inscricao.id == inscricao_id)
        .first()
    )

    if not inscricao:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")

    for campo, valor in dados.model_dump().items():
        setattr(inscricao, campo, valor)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Este e-mail já está inscrito neste evento",
        )

    db.refresh(inscricao)
    return inscricao


@app.delete("/inscricoes/{inscricao_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_inscricao(inscricao_id: int, db: Session = Depends(get_db)):
    inscricao = (
        db.query(models.Inscricao)
        .filter(models.Inscricao.id == inscricao_id)
        .first()
    )

    if not inscricao:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")

    db.delete(inscricao)
    db.commit()
