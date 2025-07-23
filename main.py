import flet as ft
from DB.database import engine, Base
from Tables.aluno import Aluno
from Tables.emprestimo import Emprestimo
from Tables.livro import Livro
from Tables.funcionario import Funcionario
#from Models.login import Login
from Models.menu_principal import MenuPrincipal

def create_tables():
    Base.metadata.create_all(engine)

def main(page: ft.Page):
    create_tables()
    MenuPrincipal(page)
    page.update()

if __name__ == "__main__":
    ft.app(target=main) 
