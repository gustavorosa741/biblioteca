from DB.database import Base
from sqlalchemy import Column, Integer, String

class Aluno(Base):
    __tablename__ = 'aluno'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    turma = Column(String(50), nullable=False)

