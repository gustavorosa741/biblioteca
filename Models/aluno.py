import flet as ft
from DB.database import session
from Tables.aluno import Aluno



def formatacao(e):
    #remove espaços e converte para maiúsculas
    e.control.value = e.control.value.upper()
    e.control.update()

class CadastroAluno:
    def __init__(self):
        self.nome = ft.TextField(
            label="Nome do Aluno",
            hint_text="Digite o nome completo",
            prefix_icon=ft.Icons.PERSON,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.idade = ft.TextField(
            label="Idade",
            hint_text="Ex: 14",
            prefix_icon=ft.Icons.CALENDAR_MONTH,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.turma = ft.TextField(
            label="Turma",
            hint_text="Ex: 8ºA",
            prefix_icon=ft.Icons.GROUP,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.status_texto = ft.Text("", size=18)

        self.botao_cadastrar = ft.ElevatedButton(
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
            on_click=self.cadastrar_aluno
        )

        self.formulario = ft.Column(
            [
                ft.Text("Cadastro de Aluno", size=32, weight=ft.FontWeight.BOLD),
                self.nome,
                self.idade,
                self.turma,
                self.botao_cadastrar,
                self.status_texto,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    def idade_int(self):
        int_idade = int(self.idade.value)
        
    def cadastrar_aluno(self, e: ft.ControlEvent):
        nome = self.nome.value
        idade = int(self.idade.value) if self.idade.value.isdigit() else None
        turma = self.turma.value

        buscar_aluno = session.query(Aluno).filter(Aluno.nome == nome).first()
        

        if not nome or not idade or not turma:
            self.status_texto.value = "Preencha todos os campos corretamente!"
            self.status_texto.color = ft.Colors.RED

        elif idade <0 or idade > 120:
            self.status_texto.value = "Idade inválida!"
            self.status_texto.color = ft.Colors.RED

        elif buscar_aluno:
            self.status_texto.value = "Aluno já cadastrado!"
            self.status_texto.color = ft.Colors.RED

        else:
            novo_aluno = Aluno(nome=nome, idade=idade, turma=turma)
            session.add(novo_aluno)
            session.commit()
            self.status_texto.value = "Aluno cadastrado com sucesso!"
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

