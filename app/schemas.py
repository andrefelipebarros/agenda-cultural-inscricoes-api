from pydantic import BaseModel, ConfigDict, EmailStr, Field


class InscricaoBase(BaseModel):
    evento_id: int = Field(gt=0)
    nome: str = Field(min_length=3, max_length=120)
    email: EmailStr
    telefone: str | None = Field(default=None, max_length=30)
    confirmada: bool = True


class InscricaoCreate(InscricaoBase):
    pass


class InscricaoUpdate(InscricaoBase):
    pass


class InscricaoResponse(InscricaoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
