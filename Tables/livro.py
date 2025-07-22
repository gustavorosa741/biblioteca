from DB.database import Base
from sqlalchemy import Column, Integer, String

class Livro(Base):
    __tablename__ = 'livros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(100), nullable=False)
    genero = Column(String(50), nullable=False)
    disponivel = Column(Integer, nullable=False, default=1)
    localizacao = Column(String(100), nullable=False)
    etiqueta = Column(String(200), nullable=False, nullable=False)

    