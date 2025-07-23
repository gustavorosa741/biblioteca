import flet as ft
from DB.database import session
from Tables.emprestimo import Emprestimo
from Tables.livro import Livro
from Tables.funcionario import Funcionario
from Tables.aluno import Aluno

def formatacao(e):
    #remove espaços e converte para maiúsculas
    e.control.value = e.control.value.upper()
    e.control.update()

class CadastroEmprestimo:
    def __init__(self):
        self.aluno = ft.TextField(
            label="Nome do Aluno",
            hint_text="Digite o nome completo do aluno",
            prefix_icon=ft.Icons.PERSON,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.etiqueta = ft.TextField(
            label="Etiqueta do Livro",
            hint_text="Digite a etiqueta do livro",
            prefix_icon=ft.Icons.TAG,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.data_emprestimo = ft.TextField(
            label="Data de Empréstimo",
            hint_text="Digite a data de empréstimo (DD/MM/AAAA)",
            prefix_icon=ft.Icons.DATE_RANGE,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.responsavel = ft.TextField(
            label="Responsável pelo Empréstimo",
            hint_text="Digite o nome do responsável",
            prefix_icon=ft.Icons.PERSON,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400
        
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
            on_click=self.cadastrar_emprestimo
        )

        self.formulario = ft.Column(
            [
                ft.Text("Cadastro de Empréstimo", size=28, weight=ft.FontWeight.BOLD),
                self.aluno,
                self.etiqueta,
                self.data_emprestimo,
                self.responsavel,
                botao_cadastrar,
                self.status_texto
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    def cadastrar_emprestimo(self, e: ft.ControlEvent):
        aluno = self.aluno.value
        etiqueta = self.etiqueta.value
        data_emprestimo = self.data_emprestimo.value
        responsavel = self.responsavel.value
        status = "Empréstimo Ativo"

        consulta_aluno = session.query(Aluno).filter_by(nome=aluno).first()
        consulta_livro = session.query(Livro).filter_by(etiqueta=etiqueta).first()
        consulta_funcionario = session.query(Funcionario).filter_by(usuario=responsavel).first()

        if not aluno or not etiqueta or not data_emprestimo or not responsavel:
            self.status_texto.value = "Todos os campos são obrigatórios."
            self.status_texto.color = ft.Colors.RED
            self.status_texto.update()
            return
        
        if not consulta_aluno:
            self.status_texto.value = "Aluno não encontrado."
            self.status_texto.color = ft.Colors.RED
            self.status_texto.update()
            return
        
        if not consulta_livro:
            self.status_texto.value = "Livro não encontrado."
            self.status_texto.color = ft.Colors.RED
            self.status_texto.update()
            return
        
        if not consulta_funcionario:
            self.status_texto.value = "Responsável não encontrado."
            self.status_texto.color = ft.Colors.RED
            self.status_texto.update()
            return

        if session.query(Emprestimo).filter_by(livro_id=consulta_livro.id).first():
            self.status_texto.value = "Empréstimo já cadastrado para esta etiqueta."
            self.status_texto.color = ft.Colors.RED
            self.status_texto.update()
            return

        else:
            consulta_livro = session.query(Livro).filter_by(etiqueta=etiqueta).first()
            novo_emprestimo = Emprestimo(
                aluno_id=consulta_aluno.id,
                livro_id=consulta_livro.id,
                data_emprestimo=data_emprestimo,
                responsavel=consulta_funcionario.id,
                status=status
            )
            session.add(novo_emprestimo)
            consulta_livro.disponivel = 0
            session.add(consulta_livro)
            session.commit()


        self.status_texto.value = "Empréstimo cadastrado com sucesso!"
        self.status_texto.color = ft.Colors.GREEN
        self.status_texto.update()

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


class CadastroDevolucao:
    def __init__(self):
        self.aluno = ft.TextField(
            label="Nome do Aluno",
            hint_text="Digite o nome completo do aluno",
            prefix_icon=ft.Icons.PERSON,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.etiqueta = ft.TextField(
            label="Etiqueta do Livro",
            hint_text="Digite a etiqueta do livro",
            prefix_icon=ft.Icons.TAG,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.data_devolucao = ft.TextField(
            label="Data de Devolução",
            hint_text="Digite a data de devolução (DD/MM/AAAA)",
            prefix_icon=ft.Icons.DATE_RANGE,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.responsavel_devolucao = ft.TextField(
            label="Responsável pela Devolução",
            hint_text="Digite o nome completo do responsável",
            prefix_icon=ft.Icons.PERSON,
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
            on_click=self.cadastrar_devolucao
        )

        self.formulario = ft.Column(
            [
                ft.Text("Cadastro de Devolução", size=28, weight=ft.FontWeight.BOLD),
                self.aluno,
                self.etiqueta,
                self.data_devolucao,
                self.responsavel_devolucao,
                botao_cadastrar,
                self.status_texto
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    def cadastrar_devolucao(self, e: ft.ControlEvent):
        aluno = self.aluno.value
        etiqueta = self.etiqueta.value
        data_devolucao = self.data_devolucao.value
        responsavel_devolucao = self.responsavel_devolucao.value
        status = "Devolução Concluída"

        consulta_aluno = session.query(Aluno).filter_by(nome=aluno).first()
        consulta_livro = session.query(Livro).filter_by(etiqueta=etiqueta).first()
        consulta_funcionario = session.query(Funcionario).filter_by(usuario=responsavel_devolucao).first()
        try:
            if not aluno or not etiqueta or not data_devolucao or not responsavel_devolucao:
                return
        except AttributeError:
            self.status_texto.value = "Todos os campos são obrigatórios."
            self.status_texto.color = ft.Colors.RED
            self.status_texto.update()
            return
        
        try:
            if not session.query(Emprestimo).filter(Emprestimo.aluno_id == consulta_aluno.id).first():
                return
        except AttributeError:
            self.status_texto.value = "Nenhum empréstimo ativo encontrado para este aluno."
            self.status_texto.color = ft.Colors.RED
            self.status_texto.update()
            return
        
        try:
            if not session.query(Emprestimo).filter(Emprestimo.livro_id == consulta_livro.id).first():
                return
        except AttributeError:
            self.status_texto.value = "Nenhum empréstimo ativo encontrado para este livro."
            self.status_texto.color = ft.Colors.RED
            self.status_texto.update()
            return
        
        try:
            if not session.query(Funcionario).filter(Funcionario.id == consulta_funcionario.id).first():
                return
        except AttributeError:
            self.status_texto.value = "Responsável não encontrado."
            self.status_texto.color = ft.Colors.RED
            self.status_texto.update()
            return
        
        emprestimo = session.query(Emprestimo).filter_by(aluno_id=consulta_aluno.id, livro_id=consulta_livro.id, status="Empréstimo Ativo").first()
        try:
            if not emprestimo:
                return
        except AttributeError:
            self.status_texto.value = "Nenhum empréstimo ativo encontrado para este aluno e livro."
            self.status_texto.color = ft.Colors.RED
            self.status_texto.update()
            return
        else:
            emprestimo.data_devolucao = data_devolucao
            emprestimo.responsavel_devolucao = consulta_funcionario.id
            emprestimo.status = status
            session.commit()

            self.status_texto.value = "Devolução cadastrada com sucesso!"
            self.status_texto.color = ft.Colors.GREEN
            self.status_texto.update()

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
        
