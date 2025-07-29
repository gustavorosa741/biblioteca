from flet import Page, Theme, ThemeMode
import flet as ft
from Models.aluno import CadastroAluno, ListaAlunos
from Models.emprestimo import CadastroEmprestimo, CadastroDevolucao
from DB.database import session

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

        def fechar_app(e):
            page.clean()
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            page.add(ft.Text("Aplicação fechada."))
            session.close()

        def abrir_cadastro_aluno(e):
            self.content_area.controls.clear()
            self.content_area.controls.append(CadastroAluno().get_container())
            page.update()

        def abrir_cadastro_livro(e):
            from Models.livro import CadastroLivro
            self.content_area.controls.clear()
            self.content_area.controls.append(CadastroLivro().get_container())
            page.update()

        def abrir_cadastro_emprestimo(e):
            self.content_area.controls.clear()
            self.content_area.controls.append(CadastroEmprestimo().get_container())
            page.update()

        def abrir_devolucao_emprestimo(e):
            self.content_area.controls.clear()
            self.content_area.controls.append(CadastroDevolucao().get_container())
            page.update()
        
        def abrir_lista_alunos(e):
            self.content_area.controls.clear()
            self.content_area.controls.append(ListaAlunos(page).get_container())
            page.update()

        def abrir_lista_livros(e):
            from Models.livro import ListaLivros
            self.content_area.controls.clear()
            self.content_area.controls.append(ListaLivros(page).get_container())
            page.update()
            
        def abrir_lista_emprestimos(e):
            from Models.emprestimo import ListarEmprestimo
            self.content_area.controls.clear()
            self.content_area.controls.append(ListarEmprestimo(page).get_container())
            page.update()

        def menu_clicked(e):
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
                            ft.PopupMenuItem(text="Novo Empréstimo", on_click=abrir_cadastro_emprestimo),
                            ft.PopupMenuItem(text="Nova Devolução", on_click=abrir_devolucao_emprestimo),
                        ]
                    ),
                    ft.PopupMenuButton(
                        content=ft.Text("Consultar", weight=ft.FontWeight.BOLD),
                        items=[
                            ft.PopupMenuItem(text="Lista de Alunos", on_click=abrir_lista_alunos),
                            ft.PopupMenuItem(text="Livros Cadastrados", on_click=abrir_lista_livros),
                        ]
                    ),
                    ft.PopupMenuButton(
                        content=ft.Text("Relatórios", weight=ft.FontWeight.BOLD),
                        items=[
                            ft.PopupMenuItem(text="Livros Emprestados", on_click=abrir_lista_emprestimos),
                        ]
                    ),
                    ft.PopupMenuButton(
                        content=ft.Text("Sair", weight=ft.FontWeight.BOLD),
                        items=[
                            ft.PopupMenuItem(text="Fechar Aplicação", on_click=lambda e: fechar_app(e)),
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

        self.content_area.controls.append(ft.Text("Bem-vindo ao sistema de biblioteca!", size=24))
        page.update()