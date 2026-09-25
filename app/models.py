from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint

from .database import Base


class Inscricao(Base):
    __tablename__ = "inscricoes"
    __table_args__ = (
        UniqueConstraint("evento_id", "email", name="uq_evento_email"),
    )

    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, nullable=False, index=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(150), nullable=False)
    telefone = Column(String(30), nullable=True)
    confirmada = Column(Boolean, nullable=False, default=True)
