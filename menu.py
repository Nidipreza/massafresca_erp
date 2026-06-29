import customtkinter as ctk

from config import COLOR_PRIMARY

from telas.pedidos import JanelaPedido
from telas.producao import JanelaProducao
from telas.expedicao import JanelaExpedicao
from telas.cadastros import JanelaCadastros
from telas.estoque import JanelaEstoque


class MenuPrincipal(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Massa Fresca ERP")

        self.geometry("500x700")

        ctk.CTkLabel(

            self,

            text="MASSA FRESCA",

            font=("Arial",32,"bold"),

            text_color=COLOR_PRIMARY

        ).pack(pady=40)

        ctk.CTkButton(

            self,

            text="📦 PEDIDOS",

            height=60,

            width=350,

            command=lambda: JanelaPedido(self)

        ).pack(pady=10)

        ctk.CTkButton(

            self,

            text="🏭 PRODUÇÃO",

            height=60,

            width=350,

            fg_color="#6a1b9a",

            command=lambda: JanelaProducao(self)

        ).pack(pady=10)

        ctk.CTkButton(

            self,

            text="📦 ESTOQUE",

            height=60,

            width=350,

            fg_color="#1565c0",

            command=lambda: JanelaEstoque(self)

        ).pack(pady=10)

        ctk.CTkButton(

            self,

            text="🚚 EXPEDIÇÃO",

            height=60,

            width=350,

            fg_color="#455a64",

            command=lambda: JanelaExpedicao(self)

        ).pack(pady=10)

        ctk.CTkButton(

            self,

            text="⚙️ CADASTROS",

            height=60,

            width=350,

            fg_color="#607d8b",

            command=lambda: JanelaCadastros(self)

        ).pack(pady=10)