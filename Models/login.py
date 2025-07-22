import flet as ft
from DB.database import session
from werkzeug.security import generate_password_hash, check_password_hash
from Tables.adm import Adm
import time

class Login:
    def __init__(self, page: ft.Page):
        page.update()
        page.window.maximized = True
        page.title = "Login"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.fonts = {"Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap"}
        page.theme = ft.Theme(font_family="Poppins")

        self.username_field = ft.TextField(
            label="Usuário",
            hint_text="Digite seu nome de usuário",
            width=300,
            border_radius=10,
            prefix_icon=ft.Icons.PERSON
        )

        self.password_field = ft.TextField(
            label="Senha",
            hint_text="Digite sua senha",
            width=300,
            password=True,
            can_reveal_password=True,
            border_radius=10,
            prefix_icon=ft.Icons.LOCK
        )

        self.error_text = ft.Text("", color=ft.Colors.RED)

        def fechar_app(e):
            page.clean()
            page.update()
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            page.add(ft.Text("Aplicação fechada."))
            session.close()

        def logar(e):
            usuario = self.username_field.value
            senha = self.password_field.value

            if not usuario or not senha:
                self.error_text.value = "Preencha todos os campos!"
                page.update()
                return

            try:
                usuario = session.query(Adm).filter_by(usuario=usuario).first()
                
                if usuario and check_password_hash(usuario.senha, senha):
                    from Models.menu_principal import MenuPrincipal
                    page.clean()
                    pass
                else:
                    self.error_text.value = "Usuário ou senha inválidos!"
                    page.update()
                    
            except Exception as e:
                self.error_text.value = f"Erro: {str(e)}"
                page.update()

        conteudo = ft.Column(
            [
                ft.Icon(ft.Icons.LOCK_PERSON, size=50),
                ft.Text("Login", size=36, weight=ft.FontWeight.BOLD),
                self.username_field,
                self.password_field,
                ft.Container(
                    ft.ElevatedButton(
                        "Entrar",
                        on_click=logar,
                        icon=ft.Icons.LOGIN,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=20,
                            bgcolor=ft.Colors.TEAL_700
                        ),
                        width=300,
                        height=50
                    ),
                    margin=ft.margin.only(top=20)
                ),
                self.error_text,
                ft.ElevatedButton(
                    "Novo Usuário",
                    on_click=lambda e: self.novo_usuario(page),
                    icon=ft.Icons.PERSON_ADD,
                    style=ft.ButtonStyle(color=ft.Colors.TEAL),
                    width=300,
                    height=50
                ),
                ft.TextButton(
                    "Fechar Aplicação",
                    on_click=fechar_app,
                    icon=ft.Icons.EXIT_TO_APP,
                    style=ft.ButtonStyle(color=ft.Colors.RED))
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20)
        page.clean()
        page.add(
    ft.Stack(
        [
            ft.Container(
                gradient=ft.LinearGradient(
                    colors=[ft.Colors.BLUE, ft.Colors.BLACK],
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center
                ),
                expand=True
            ),
            
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=conteudo,
                        padding=40,
                        width=500,
                        height=600,
                        border_radius=20,

                        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
                    ),
                    elevation=20,
                    shape=ft.RoundedRectangleBorder(radius=20),
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ],
        expand=True
    )
)

    def novo_usuario(self, page: ft.Page):
        page.update()
        page.window.maximized = True
        page.title = "Novo Usuário"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.fonts = {"Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap"}
        page.theme = ft.Theme(font_family="Poppins")
        aviso = ft.Text("", color=ft.Colors.RED)


        usuario = ft.TextField(
            label="Usuário",
            hint_text="Digite seu nome de usuário",
            width=300,
            border_radius=10,
            prefix_icon=ft.Icons.PERSON
        )

        senha = ft.TextField(
            label="Senha",
            hint_text="Digite sua senha",
            width=300,
            password=True,
            can_reveal_password=True,
            border_radius=10,
            prefix_icon=ft.Icons.LOCK
        )

        confirmar_senha = ft.TextField(
            label="Confirme sua senha",
            hint_text="Digite sua senha",
            width=300,
            password=True,
            can_reveal_password=True,
            border_radius=10,
            prefix_icon=ft.Icons.LOCK
        )

        def voltar(e):
            self.__init__(page)
            page.update()

        def cadastrar(e):
            if not all ([usuario.value, senha.value, confirmar_senha.value]):
                aviso.value = "Preencha todos os campos"
                page.update()
                return
            
            if len (senha.value) < 8:
                aviso.value = "A senha deve ter no mínimo 8 caracteres"
                page.update()
                return
            
            if senha.value != confirmar_senha.value:
                aviso.value = "As senhas não são iguais"
                page.update()
                return
            
            verificar_usuario = session.query(Adm).filter_by(usuario=usuario.value).first()
            try:
                if verificar_usuario:
                    aviso.value = "Usuario ja existe"
                    aviso.color = ft.Colors.RED

                    page.update()
                    return
                novo_usuario = Adm(usuario=usuario.value, senha=generate_password_hash(senha.value))
                session.add(novo_usuario)
                session.commit()

                aviso.value = "Usuario cadastrado com sucesso"
                aviso.color = ft.Colors.GREEN
                page.update()
                time.sleep(1)
                self.__init__(page)

            except Exception as e:
                aviso.value = f"Erro: {str(e)}"
                page.update()

        page.clean()
        login_form = ft.Column(
            [
                ft.Icon(ft.Icons.LOCK_PERSON, size=50),
                ft.Text("Novo Usuario", size=36, weight=ft.FontWeight.BOLD),
                usuario,
                senha,
                confirmar_senha,
                ft.Container(
                    ft.ElevatedButton(
                        "Cadastrar",
                        on_click=cadastrar,
                        icon=ft.Icons.ADD,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=20,
                            bgcolor=ft.Colors.TEAL_700
                        ),
                        width=300,
                        height=50
                    ),
                    margin=ft.margin.only(top=20)
                ),
                aviso,
                ft.TextButton(
                    "Voltar",
                    on_click=voltar,
                    icon=ft.Icons.EXIT_TO_APP,
                    style=ft.ButtonStyle(color=ft.Colors.RED))
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20)

        page.add(
    ft.Stack(
        [
            ft.Container(
                gradient=ft.LinearGradient(
                    colors=[ft.Colors.BLUE, ft.Colors.BLACK],
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center
                ),
                expand=True
            ),
            
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=login_form,
                        padding=40,
                        width=500,
                        height=600,
                        border_radius=20,

                        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
                    ),
                    elevation=20,
                    shape=ft.RoundedRectangleBorder(radius=20),
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ],
        expand=True
    )
)
            

