import flet as ft
from DB.database import engine, Base
from Tables.aluno import Aluno
from Tables.emprestimo import emprestimo
from Tables.livro import Livro
from Tables.adm import Adm
from Models.login import Login

def create_tables():
    Base.metadata.create_all(engine)

def main(page: ft.Page):
    create_tables()
    Login(page)
    page.update()

if __name__ == "__main__":
    ft.app(target=main) 
