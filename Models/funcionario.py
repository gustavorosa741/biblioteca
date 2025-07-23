import flet as ft


class Funcionario:
    def __init__(self):
        self.nome = ft.TextField(
            label="Nome do Funcionário",
            hint_text="Digite o nome completo do funcionário",
            prefix_icon=ft.Icons.PERSON,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400
        )

        self.usuario = ft.TextField(
            label="Usuário",
            hint_text="Digite o nome de usuário",
            prefix_icon=ft.Icons.ACCOUNT_CIRCLE,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400
        )

        self.senha = ft.TextField(
            label="Senha",
            hint_text="Digite a senha",
            prefix_icon=ft.Icons.LOCK,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            password=True
        )

    def get_container(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.nome, 
                    self.usuario, 
                    self.senha
                ],
                spacing=20
            ),
            padding=20
        )