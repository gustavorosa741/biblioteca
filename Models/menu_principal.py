from flet import Page, Theme, ThemeMode
import flet as ft
from Models.aluno import CadastroAluno

def menu_clicked(e):
    pass

class MenuPrincipal:
    def __init__(self, page: Page):
        page.title = "Menu Principal"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.vertical_alignment = ft.MainAxisAlignment.START  # Alinha tudo no topo

        menu_superior = ft.Container(
        content=ft.Row(
            controls=[
                ft.PopupMenuButton(
                    content=ft.Text("Cadastrar", weight=ft.FontWeight.BOLD),
                    items=[
                        ft.PopupMenuItem(text="Novo Aluno", on_click= lambda e: CadastroAluno(page)),
                        ft.PopupMenuItem(text="Novo Livro", on_click=menu_clicked),
                        ft.PopupMenuItem(text="Novo Funcionário", on_click=menu_clicked),
                    ]
                ),
                ft.PopupMenuButton(
                    content=ft.Text("Consultar", weight=ft.FontWeight.BOLD),
                    items=[
                        ft.PopupMenuItem(text="Lista de Alunos", on_click=menu_clicked),
                        ft.PopupMenuItem(text="Livros Cadastrados", on_click=menu_clicked),
                        ft.PopupMenuItem(text="Funcionários", on_click=menu_clicked),
                        
                    ]
                ),
                ft.PopupMenuButton(
                    content=ft.Text("Relatórios", weight=ft.FontWeight.BOLD),
                    items=[
                        ft.PopupMenuItem(text="Livros Emprestados", on_click=menu_clicked),
                        ft.PopupMenuItem(text="Histórico de Alunos", on_click=menu_clicked),

                    ]
                ),
                ft.PopupMenuButton(
                    content=ft.Text("Sair", weight=ft.FontWeight.BOLD),
                    items=[
                        ft.PopupMenuItem(text="Fechar Aplicação", on_click=lambda e: page.close()),
                        ft.PopupMenuItem(text="Sair do Sistema",  on_click=menu_clicked),
                        
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20
        ),
        padding=10,
        bgcolor=ft.Colors.BLUE_700,  # Fundo azul claro
        border_radius=5
    )

        # Conteúdo principal da tela
        page.add(
            ft.Column(
                [
                    menu_superior,
                    ft.Divider(thickness=2),
                    ft.Text("Bem-vindo ao sistema de biblioteca!", size=24),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True
            )
        )