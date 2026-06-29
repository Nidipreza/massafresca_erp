import customtkinter as ctk

from conexao import supabase

from config import (
    COLOR_PRIMARY,
    COLOR_BG_APP,
    COLOR_BG_CARD,
)


class JanelaEstoque(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Estoque da Expedição")

        self.after(
            0,
            lambda: self.state("zoomed")
        )

        self.configure(
            fg_color=COLOR_BG_APP
        )

        self.grab_set()

        self.lista_produtos = []

        ctk.CTkLabel(
            self,
            text="📦 ESTOQUE DA EXPEDIÇÃO",
            font=("Arial", 28, "bold"),
            text_color=COLOR_PRIMARY
        ).pack(
            pady=20
        )

        self.busca = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="Pesquisar produto..."
        )

        self.busca.pack(
            pady=10
        )

        self.busca.bind(
            "<KeyRelease>",
            self.filtrar
        )

        self.lbl_resumo = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 15, "bold")
        )

        self.lbl_resumo.pack(
            pady=10
        )

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.carregar()

    # ----------------------------------------

    def carregar(self):

        resposta = (
            supabase
            .table("Produtos")
            .select("*")
            .eq("ativo", True)
            .eq("categoria", "EXPEDICAO")
            .order("nome")
            .execute()
        )

        self.lista_produtos = resposta.data or []

        self.atualizar_resumo()

        self.renderizar(
            self.lista_produtos
        )

    # ----------------------------------------

    def atualizar_resumo(self):

        total = len(self.lista_produtos)

        abaixo = 0

        zerados = 0

        for p in self.lista_produtos:

            estoque = p.get("estoque_atual") or 0

            minimo = p.get("estoque_minimo") or 0

            if estoque == 0:
                zerados += 1

            if estoque < minimo:
                abaixo += 1

        self.lbl_resumo.configure(

            text=(
                f"Produtos: {total}      "
                f"Abaixo do mínimo: {abaixo}      "
                f"Zerados: {zerados}"
            )

        )

    # ----------------------------------------

    def filtrar(self, event=None):

        texto = self.busca.get().lower()

        if texto == "":

            self.renderizar(
                self.lista_produtos
            )

            return

        filtrado = []

        for produto in self.lista_produtos:

            nome = (
                produto.get("nome") or ""
            ).lower()

            if texto in nome:

                filtrado.append(produto)

        self.renderizar(
            filtrado
        )

    # ----------------------------------------

    def renderizar(self, lista):

        for w in self.scroll.winfo_children():

            w.destroy()

        for produto in lista:

            self.criar_card(produto)

    # ----------------------------------------

    def criar_card(self, produto):

        card = ctk.CTkFrame(

            self.scroll,

            fg_color=COLOR_BG_CARD,

            corner_radius=12,

            border_width=1

        )

        card.pack(

            fill="x",

            padx=5,

            pady=8

        )

        nome = produto.get("nome")

        estoque = produto.get("estoque_atual") or 0

        minimo = produto.get("estoque_minimo") or 0

        faltam = max(
            0,
            minimo - estoque
        )

        percentual = 1

        if minimo > 0:

            percentual = estoque / minimo

        percentual = min(
            percentual,
            1
        )

        ctk.CTkLabel(

            card,

            text=nome,

            font=("Arial", 18, "bold")

        ).pack(

            anchor="w",

            padx=20,

            pady=(15, 5)

        )

        ctk.CTkLabel(

            card,

            text=f"Estoque Atual: {estoque}"

        ).pack(

            anchor="w",

            padx=20

        )

        ctk.CTkLabel(

            card,

            text=f"Estoque Mínimo: {minimo}"

        ).pack(

            anchor="w",

            padx=20

        )

        if faltam > 0:

            texto = f"⚠️ Faltam {faltam} unidades"

            cor = "#d35400"

        else:

            texto = "✅ Estoque mínimo atingido"

            cor = "#2e7d32"

        ctk.CTkLabel(

            card,

            text=texto,

            text_color=cor,

            font=("Arial", 14, "bold")

        ).pack(

            anchor="w",

            padx=20,

            pady=(5, 5)

        )

        barra = ctk.CTkProgressBar(

            card,

            height=18

        )

        barra.pack(

            fill="x",

            padx=20,

            pady=10

        )

        barra.set(percentual)

        ctk.CTkLabel(

            card,

            text=f"{int(percentual*100)}% do estoque mínimo"

        ).pack(

            pady=(0, 15)

        )