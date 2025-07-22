from flet import Page, Theme, ThemeMode
import flet as ft
from Models.aluno import CadastroAluno

def menu_clicked(e):
    pass

class MenuPrincipal:
    def __init__(self, page: ft.Page):
        page.title = "Menu Principal"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.vertical_alignment = ft.MainAxisAlignment.START

        self.page = page
        self.content_area = ft.Column(expand=True)

        def abrir_cadastro_aluno(e):
            self.content_area.controls.clear()
            self.content_area.controls.append(CadastroAluno().get_container())
            page.update()

        def abrir_cadastro_livro(e):
            from Models.livro import CadastroLivro
            self.content_area.controls.clear()
            self.content_area.controls.append(CadastroLivro().get_container())
            page.update()

        def menu_clicked(e):
            # Ação padrão para os demais itens
            self.content_area.controls.clear()
            self.content_area.controls.append(ft.Text(f"Clicou em: {e.control.text}"))
            page.update()

        menu_superior = ft.Container(
            content=ft.Row(
                controls=[
                    ft.PopupMenuButton(
                        content=ft.Text("Cadastrar", weight=ft.FontWeight.BOLD),
                        items=[
                            ft.PopupMenuItem(text="Novo Aluno", on_click=abrir_cadastro_aluno),
                            ft.PopupMenuItem(text="Novo Livro", on_click=abrir_cadastro_livro),
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
                            ft.PopupMenuItem(text="Sair do Sistema", on_click=menu_clicked),
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20
            ),
            padding=10,
            bgcolor=ft.Colors.BLUE_700,
            border_radius=5
        )

        # Adiciona os elementos na tela
        page.add(
            ft.Column(
                [
                    menu_superior,
                    ft.Divider(thickness=2),
                    self.content_area
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True
            )
        )

        # Mensagem inicial
        self.content_area.controls.append(ft.Text("Bem-vindo ao sistema de biblioteca!", size=24))
        page.update()