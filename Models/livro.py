import flet as ft
from DB.database import session
from Tables.livro import Livro

def formatacao(e):
    #remove espaços e converte para maiúsculas
    e.control.value = e.control.value.upper()
    e.control.update()

class CadastroLivro:
    def __init__(self):
        self.nome = ft.TextField(
            label="Nome do Livro",
            hint_text="Digite o nome completo do livro",
            prefix_icon=ft.Icons.BOOK,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.autor = ft.TextField(
            label="Autor",
            hint_text="Digite o nome do autor",
            prefix_icon=ft.Icons.PERSON,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.genero = ft.TextField(
            label="Gênero",
            hint_text="Ex: Ficção, Aventura",
            prefix_icon=ft.Icons.LIBRARY_BOOKS,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.localizacao = ft.TextField(
            label="Localização",
            hint_text="Ex: Prateleira 1, Seção A",
            prefix_icon=ft.Icons.LOCATION_ON,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.etiqueta = ft.TextField(
            label="Etiqueta",
            hint_text="Ex: LIV12345",
            prefix_icon=ft.Icons.TAG,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.status_texto = ft.Text("", size=18)

        botao_cadastrar = ft.ElevatedButton(
            text="Cadastrar",
            icon=ft.Icons.CHECK_CIRCLE,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20,
            ),
            width=400,
            height=50,
            on_click=self.cadastrar_livro
        )

        self.formulario = ft.Column(
            [
                ft.Text("Cadastro de Livro", size=32, weight=ft.FontWeight.BOLD),
                self.nome,
                self.autor,
                self.genero,
                self.localizacao,
                self.etiqueta,
                botao_cadastrar,
                self.status_texto,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    def cadastrar_livro(self, e: ft.ControlEvent):
        nome = self.nome.value
        autor = self.autor.value
        genero = self.genero.value
        localizacao = self.localizacao.value
        etiqueta = self.etiqueta.value

        if not nome or not autor or not genero or not localizacao or not etiqueta:
            self.status_texto.value = "Preencha todos os campos corretamente!"
            self.status_texto.color = ft.Colors.RED
            self.status_texto.update()
            return

        if session.query(Livro).filter_by(etiqueta=etiqueta).first():
            self.status_texto.value = "Livro já cadastrada!"
            self.status_texto.color = ft.Colors.RED
            self.status_texto.update()
            return
        
        else:
            novo_livro = Livro(
                titulo=nome,
                autor=autor,
                genero=genero,
                disponivel=1,
                localizacao=localizacao,
                etiqueta=etiqueta
            )
        session.add(novo_livro)
        session.commit()

        self.status_texto.value = "Livro cadastrado com sucesso!"
        self.status_texto.color = ft.Colors.GREEN

        e.page.update()

    def get_container(self):
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=self.formulario,
                    padding=40,
                    width=500,
                    border_radius=20,
                    bgcolor=ft.Colors.WHITE,
                ),
                elevation=10,
                shape=ft.RoundedRectangleBorder(radius=20),
            ),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.Colors.BLUE_100
        )

    

        