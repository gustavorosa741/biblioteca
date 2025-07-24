import flet as ft
from flet import DataColumn, DataCell, DataRow, SearchBar
from sqlalchemy import or_
from DB.database import session
from Tables.livro import Livro

def formatacao(e):
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

class ListaLivros:
    def __init__(self, page: ft.Page):
        self.page = page
        self.status_texto = ft.Text("", size=18)
        self.dialog = ft.AlertDialog(modal=True)

        self.barra_pesquisa = SearchBar(
            bar_hint_text="Buscar livros por nome, autor, gênero ou etiqueta",
            view_hint_text="Digite termos para buscar...",
            on_change=self.filtrar_livros,
            on_submit=self.filtrar_livros,
            width=420,
            height=40,
        )

        self.disponiveis = None
        self.filtro_disponiveis = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    text="Todos os livros", 
                    on_click=self.disponivel_todos,
                    checked=lambda: self.disponiveis is None,
                ),
                ft.PopupMenuItem(
                    text="Disponíveis", 
                    on_click=self.disponivel_disponivel,
                    checked=lambda: self.disponiveis == 1,
                ),
                ft.PopupMenuItem(
                    text="Indisponíveis", 
                    on_click=self.disponiveo_indisponivel,
                    checked=lambda: self.disponiveis == 0,
                ),
            ],
            icon=ft.Icons.FILTER_LIST,
            tooltip="Filtrar livros",
        )

        self.tabela_livros = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Autor")),
                ft.DataColumn(ft.Text("Gênero")),
                ft.DataColumn(ft.Text("Etiqueta")),
                ft.DataColumn(ft.Text("Localização")),
                ft.DataColumn(ft.Text("Disponibilidade")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.BLACK),
            heading_row_color=ft.Colors.BLUE_100,
            data_row_color=ft.Colors.WHITE,
            heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD)
        )

        self.formulario = ft.Column(
            [
                ft.Text("📚 Lista de Livros", size=28, weight=ft.FontWeight.BOLD),
                ft.Row([self.barra_pesquisa, self.filtro_disponiveis], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    content=self.tabela_livros,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=10,
                    padding=10,
                ),
                self.status_texto,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
            scroll=ft.ScrollMode.AUTO
        )

        self.atualizar_lista()

    def gerar_linha_tabela(self, livro: Livro):
        return DataRow(
            cells=[
                DataCell(ft.Text(str(livro.id))),
                DataCell(ft.Text(livro.titulo)),
                DataCell(ft.Text(livro.autor)),
                DataCell(ft.Text(livro.genero)),
                DataCell(ft.Text(livro.etiqueta)),
                DataCell(ft.Text(livro.localizacao)),
                DataCell(ft.Text("Disponível" if livro.disponivel else "Indisponível")),
                DataCell(
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar Livro",
                                on_click=lambda e, livro=livro: self.editar_livro(e, livro)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Excluir Livro",
                                on_click=lambda e, livro=livro: self.excluir_livro(e, livro)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
            ]
        )
    
    def editar_livro(self, e, livro: Livro):
        self.dialog.title = "Editar Livro"
        self.dialog.content = ft.Column(
            [
                ft.TextField(label="Nome", value=livro.titulo, on_change=formatacao),
                ft.TextField(label="Autor", value=livro.autor, on_change=formatacao),
                ft.TextField(label="Gênero", value=livro.genero, on_change=formatacao),
                ft.TextField(label="Localização", value=livro.localizacao, on_change=formatacao),
                ft.TextField(label="Etiqueta", value=livro.etiqueta, on_change=formatacao),
            ],
            spacing=10
        )
        self.dialog.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: self.fechar_dialog(e)),
            ft.TextButton("Salvar", on_click=lambda e: self.confirmar_edicao(livro))
        ]
        self.page.open(self.dialog)
        self.page.update()

    def confirmar_edicao(self, livro: Livro):
        livro.titulo = self.dialog.content.controls[0].value
        livro.autor = self.dialog.content.controls[1].value
        livro.genero = self.dialog.content.controls[2].value
        livro.localizacao = self.dialog.content.controls[3].value
        livro.etiqueta = self.dialog.content.controls[4].value

        session.commit()
        self.page.close(self.dialog)
        self.atualizar_lista()
        self.page.update()

    def excluir_livro(self, e, livro: Livro):
        self.dialog.title = "Excluir Livro"
        self.dialog.content = ft.Text(f"Você tem certeza que deseja excluir o livro '{livro.titulo}'?")
        self.dialog.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: self.fechar_dialog(e)),
            ft.TextButton("Excluir", on_click=lambda e: self.confirmar_exclusao(livro))
        ]
        self.page.update()
        self.page.open(self.dialog)

    def confirmar_exclusao(self, livro: Livro):
        session.delete(livro)
        session.commit()
        self.page.close(self.dialog)
        self.atualizar_lista()
        self.page.update()
        
    def fechar_dialog(self, e):
        self.page.close(self.dialog)
        self.page.update()
    
    def disponivel_todos(self, e):
        self.disponiveis = None
        self.filtrar_livros(e)
        self.page.update()

    def disponivel_disponivel(self, e):
        self.disponiveis = 1
        self.filtrar_livros(e)
        self.page.update()

    def disponiveo_indisponivel(self, e):
        self.disponiveis = 0
        self.filtrar_livros(e)
        self.page.update()

    def filtrar_livros(self, e):
        termo_busca = self.barra_pesquisa.value.strip().lower() if self.barra_pesquisa.value else ""
        
        query = session.query(Livro)

        if termo_busca:
            query = query.filter(
                or_(
                    Livro.titulo.ilike(f"%{termo_busca}%"),
                    Livro.autor.ilike(f"%{termo_busca}%"),
                    Livro.genero.ilike(f"%{termo_busca}%"),
                    Livro.etiqueta.ilike(f"%{termo_busca}%"),
                    Livro.localizacao.ilike(f"%{termo_busca}%"),
                )
            )

        if self.disponiveis is not None:
            query = query.filter(Livro.disponivel == self.disponiveis)

        livros_filtrados = query.all()
        
        self.tabela_livros.rows = [
            self.gerar_linha_tabela(livro) 
            for livro in livros_filtrados
        ]

        if not livros_filtrados:
            self.status_texto.value = "Nenhum livro encontrado."
            self.status_texto.color = ft.Colors.RED
        else:
            self.status_texto.value = f"{len(livros_filtrados)} livro(s) encontrado(s)."
            self.status_texto.color = ft.Colors.GREEN

        if e is not None:
            self.page.update()

    def atualizar_lista(self):
        self.filtrar_livros(None)
        livros = session.query(Livro).all()
        self.tabela_livros.rows.clear()

        for livro in livros:
            self.tabela_livros.rows.append(self.gerar_linha_tabela(livro))

        if not livros:
            self.status_texto.value = "Nenhum livro cadastrado."
            self.status_texto.color = ft.Colors.RED
        else:
            self.status_texto.value = f"{len(livros)} livro(s) cadastrado(s)."
            self.status_texto.color = ft.Colors.GREEN

        self.page.update()

    def get_container(self):
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=self.formulario,
                    padding=40,
                    width=1200,
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