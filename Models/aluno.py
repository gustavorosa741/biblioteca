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

class ListaAlunos:
    def __init__(self):
        self.status_texto = ft.Text("", size=18)

        self.filtro_nome = ft.TextField(
            label="Buscar por nome",
            prefix_icon=ft.Icons.SEARCH,
            width=400,
            on_change=lambda e: self.atualizar_lista()
        )

        self.filtro_turma = ft.Dropdown(
            label="Filtrar por turma",
            width=400,
            on_change=lambda e: self.atualizar_lista(),
            hint_text="Todas as turmas"
        )

        self.lista_view = ft.ListView(
            spacing=5,
            padding=5,
            auto_scroll=False,
            expand=True
        )

        self.dialog = ft.AlertDialog(modal=True)

        self.formulario = ft.Column(
            [
                ft.Text("📋 Lista de Alunos", size=28, weight=ft.FontWeight.BOLD),
                ft.Row([self.filtro_nome, self.filtro_turma], spacing=20),
                self.lista_view,
                self.status_texto
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        self.alunos = session.query(Aluno).order_by(Aluno.nome).all()
        turmas = sorted({aluno.turma for aluno in self.alunos})
        self.filtro_turma.options = [ft.dropdown.Option(t) for t in turmas]

        self.atualizar_lista()

    def gerar_cartao(self, aluno: Aluno):
        return ft.Card(
            elevation=3,
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(aluno.nome, size=20, weight=ft.FontWeight.BOLD),
                        ft.IconButton(icon=ft.Icons.INFO, tooltip="Detalhes", on_click=lambda e: self.mostrar_detalhes(aluno)),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(f"Idade: {aluno.idade}"),
                    ft.Text(f"Turma: {aluno.turma}"),
                    ft.Row([
                        ft.ElevatedButton("Editar", icon=ft.Icons.EDIT, on_click=lambda e: self.editar_aluno(aluno)),
                        ft.OutlinedButton("Excluir", icon=ft.Icons.DELETE, on_click=lambda e: self.confirmar_exclusao(aluno)),
                    ], spacing=5),
                ]),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                animate=ft.Animation(300, "easeInOut"),
                on_hover=lambda e: (setattr(e.control, "bgcolor", ft.Colors.BLUE_50 if e.data == "true" else ft.Colors.WHITE), e.control.update())
            )
        )

    def mostrar_detalhes(self, aluno: Aluno):
        self.dialog.title = ft.Text(f"Detalhes de {aluno.nome}")
        self.dialog.content = ft.Column([
            ft.Text(f"ID: {aluno.id}"),
            ft.Text(f"Nome: {aluno.nome}"),
            ft.Text(f"Idade: {aluno.idade}"),
            ft.Text(f"Turma: {aluno.turma}"),
        ])
        self.dialog.actions = [ft.TextButton("Fechar", on_click=lambda e: setattr(self.dialog, 'open', False))]
        self.dialog.actions_alignment = ft.MainAxisAlignment.END
        self.dialog.open = True

    def editar_aluno(self, aluno: Aluno):
        print(f"Editar aluno: {aluno.id} - {aluno.nome}")
        self.status_texto.value = f"Edição futura: {aluno.nome}"
        self.status_texto.color = ft.Colors.AMBER
        self.status_texto.update()

    def confirmar_exclusao(self, aluno: Aluno):
        self.dialog.title = ft.Text("Confirmar exclusão")
        self.dialog.content = ft.Text(f"Deseja realmente excluir {aluno.nome}?")
        self.dialog.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: setattr(self.dialog, 'open', False)),
            ft.TextButton("Excluir", style=ft.ButtonStyle(color=ft.Colors.RED), on_click=lambda e: self.excluir_aluno(aluno))
        ]
        self.dialog.actions_alignment = ft.MainAxisAlignment.CENTER
        self.dialog.open = True

    def excluir_aluno(self, aluno: Aluno):
        session.delete(aluno)
        session.commit()
        self.dialog.open = False
        self.status_texto.value = f"Aluno '{aluno.nome}' excluído com sucesso."
        self.status_texto.color = ft.Colors.GREEN
        self.status_texto.update()
        self.alunos = session.query(Aluno).order_by(Aluno.nome).all()
        self.atualizar_lista()

    def atualizar_lista(self):
        nome_filtro = self.filtro_nome.value.lower() if self.filtro_nome.value else ""
        turma_filtro = self.filtro_turma.value

        self.lista_view.controls.clear()
        for aluno in self.alunos:
            if nome_filtro and nome_filtro not in aluno.nome.lower():
                continue
            if turma_filtro and aluno.turma != turma_filtro:
                continue
            self.lista_view.controls.append(self.gerar_cartao(aluno))

    def get_container(self):
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=self.formulario,
                    padding=40,
                    width=900,
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
