import flet as ft
from flet import DataColumn, DataCell, DataRow
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

class ListaLivros:
    def __init__(self, page: ft.Page):
        self.page = page
        self.status_texto = ft.Text("", size=18)
        self.dialog = ft.AlertDialog(modal=True)

        self.tabela_livros = ft.DataTable(
            columns=[
                DataColumn(label=ft.Text("ID")),
                DataColumn(label=ft.Text("Nome")),
                DataColumn(label=ft.Text("Autor")),
                DataColumn(label=ft.Text("Gênero")),
                DataColumn(label=ft.Text("Etiqueta")),
                DataColumn(label=ft.Text("Localização")),
                DataColumn(label=ft.Text("Disponibilidade")),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.BLACK),
            heading_row_color=ft.Colors.BLUE_100,
            data_row_color=ft.Colors.WHITE,
            heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD)
        )
        
        self.filtro_nome = ft.TextField(
            label="Nome",
            hint_text="Digite o nome do livro",
            prefix_icon=ft.Icons.SEARCH,
            width=150,
            on_change=self.filtrar_livros
        )

        self.filtro_autor = ft.TextField(
            label="Autor",
            prefix_icon=ft.Icons.SEARCH,
            width=150,
            on_change=self.filtrar_livros
        )

        self.filtro_genero = ft.TextField(
            label="Gênero",
            prefix_icon=ft.Icons.SEARCH,
            width=150,
            on_change=self.filtrar_livros
        )

        self.filtro_etiqueta = ft.TextField(
            label="Etiqueta",
            prefix_icon=ft.Icons.SEARCH,
            width=150,
            on_change=self.filtrar_livros
        )

        self.filtro_localizacao = ft.TextField(
            label="Localização",
            prefix_icon=ft.Icons.SEARCH,
            width=150,
            on_change=self.filtrar_livros
        )

        self.filtro_disponibilidade = ft.Dropdown(
            label="Disponibilidade",
            options=[
                ft.dropdown.Option(text="Disponível"),
                ft.dropdown.Option(text="Indisponível"),
                ft.dropdown.Option(text="Todos"),
            ],
            width=150,
            on_change=self.filtrar_livros, 
        )

        self.tabela_buscar_livros = ft.Row(
            controls=[
                self.filtro_nome,
                self.filtro_autor,
                self.filtro_genero,
                self.filtro_etiqueta,
                self.filtro_localizacao,
                self.filtro_disponibilidade,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        self.formulario = ft.Column(
            [
                ft.Text("📚 Lista de Livros", size=28, weight=ft.FontWeight.BOLD),
                self.tabela_buscar_livros,
                self.tabela_livros,
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
            ]
        )

    def filtrar_livros(self, e):
        nome = self.filtro_nome.value.lower()
        autor = self.filtro_autor.value.lower()
        genero = self.filtro_genero.value.lower()
        etiqueta = self.filtro_etiqueta.value.lower()
        localizacao = self.filtro_localizacao.value.lower()
        disponibilidade = self.filtro_disponibilidade.value.lower()

        query = session.query(Livro)

        if nome:
            query = query.filter(Livro.titulo.ilike(f"%{nome}%"))

        if autor:
            query = query.filter(Livro.autor.ilike(f"%{autor}%"))

        if genero:
            query = query.filter(Livro.genero.ilike(f"%{genero}%"))

        if etiqueta:
            query = query.filter(Livro.etiqueta.ilike(f"%{etiqueta}%"))

        if localizacao:
            query = query.filter(Livro.localizacao.ilike(f"%{localizacao}%"))
        
        if disponibilidade == "disponível":
            query = query.filter(Livro.disponivel == 1)

        elif disponibilidade == "indisponível":
            query = query.filter(Livro.disponivel == 0)

        else:
            query = query.filter(Livro.disponivel.in_([0, 1]))

        livros_filtrados = query.all()
        self.tabela_livros.rows.clear()

        for livro in livros_filtrados:
            self.tabela_livros.rows.append(self.gerar_linha_tabela(livro))

        if not livros_filtrados:
            self.status_texto.value = "Nenhum livro encontrado."
            self.status_texto.color = ft.Colors.RED
        else:
            self.status_texto.value = f"{len(livros_filtrados)} livro(s) encontrado(s)."
            self.status_texto.color = ft.Colors.GREEN

        self.page.update()

    def atualizar_lista(self):
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