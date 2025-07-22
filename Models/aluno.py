import flet as ft

class CadastroAluno:
    def __init__(self, page: ft.Page):
        page.title = "Cadastro de Aluno"
        page.padding = 0
        page.window_maximized = True
        page.theme_mode = ft.ThemeMode.LIGHT
        page.fonts = {
            "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap"
        }
        page.theme = ft.Theme(font_family="Poppins")

        # Campos do formulário
        self.nome = ft.TextField(
            label="Nome do Aluno",
            hint_text="Digite o nome completo",
            prefix_icon=ft.Icons.PERSON,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400
        )

        self.idade = ft.TextField(
            label="Idade",
            hint_text="Ex: 14",
            prefix_icon=ft.Icons.CALENDAR_MONTH,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400
        )

        self.turma = ft.TextField(
            label="Turma",
            hint_text="Ex: 8ºA",
            prefix_icon=ft.Icons.GROUP,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400
        )

        self.status_texto = ft.Text("", size=16)

        # Botão de cadastro
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

        # Container do formulário centralizado
        formulario = ft.Column(
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

        # Layout com fundo claro e centro branco
        page.add(
            ft.Stack([
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.BLUE_100
                ),
                ft.Container(
                    content=ft.Card(
                        content=ft.Container(
                            content=formulario,
                            padding=40,
                            width=500,
                            border_radius=20,
                            bgcolor=ft.Colors.WHITE,
                        ),
                        elevation=10,
                        shape=ft.RoundedRectangleBorder(radius=20)
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ])
        )

    def cadastrar_aluno(self, e):
        # Aqui você pode aplicar sua lógica de banco
        nome = self.nome.value
        idade = self.idade.value
        turma = self.turma.value

        if not nome or not idade or not turma:
            self.status_texto.value = "Preencha todos os campos!"
            self.status_texto.color = ft.Colors.RED
        else:
            self.status_texto.value = "Aluno cadastrado com sucesso!"
            self.status_texto.color = ft.Colors.GREEN

        e.page.update()