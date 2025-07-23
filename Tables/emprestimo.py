from DB.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date

class Emprestimo(Base):
    __tablename__ = 'emprestimos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aluno_id = Column(Integer, ForeignKey("aluno.id"), nullable=False)
    livro_id = Column(Integer, ForeignKey("livro.id"), nullable=False)
    data_emprestimo = Column(Date, nullable=False)
    data_devolucao = Column(Date, nullable=True)
    status = Column(String(20), nullable=False)
    responsavel = Column(Integer, ForeignKey("funcionario.id"), nullable=False)
    responsavel_devolucao = Column(Integer, ForeignKey("funcionario.id"), nullable=True)

    