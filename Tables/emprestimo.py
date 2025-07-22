from DB.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date

class emprestimo(Base):
    __tablename__ = 'emprestimos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aluno_id = Column(Integer, ForeignKey("aluno.id"), nullable=False)
    livro_id = Column(Integer, ForeignKey("livro.id"), nullable=False)
    data_emprestimo = Column(Date, nullable=False)
    data_devolucao = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default='ativo')  # ativo, devolvido, atrasado