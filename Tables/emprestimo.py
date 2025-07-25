from DB.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

class Emprestimo(Base):
    __tablename__ = 'emprestimos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aluno_id = Column(Integer, ForeignKey("aluno.id", ondelete="SET NULL"), nullable=True)
    livro_id = Column(Integer, ForeignKey("livro.id", ondelete="SET NULL"), nullable=True)
    data_emprestimo = Column(Date, nullable=False)
    data_devolucao = Column(Date, nullable=True)
    status = Column(String(20), nullable=False)
    responsavel = Column(Integer, ForeignKey("funcionario.id", ondelete="SET NULL"), nullable=True)
    responsavel_devolucao = Column(Integer, ForeignKey("funcionario.id", ondelete="SET NULL"), nullable=True)

    aluno = relationship("Aluno", backref="emprestimos", passive_deletes=True)
    livro = relationship("Livro", backref="emprestimos", passive_deletes=True)
    funcionario_responsavel = relationship("Funcionario", foreign_keys=[responsavel], passive_deletes=True)
    funcionario_devolucao = relationship("Funcionario", foreign_keys=[responsavel_devolucao], passive_deletes=True)
