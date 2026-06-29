import customtkinter as ctk
import tkinter.messagebox as messagebox
from datetime import datetime

from conexao import supabase

from config import (
    COLOR_PRIMARY,
    COLOR_SUCCESS,
    COLOR_BG_APP,
    COLOR_BG_CARD,
)


class JanelaProducao(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Produção")
        
        self.after(0, lambda: self.state("zoomed"))
        self.configure(fg_color=COLOR_BG_APP)
        self.grab_set()

        self.lista_produtos = []

        self.somente_faltantes = ctk.BooleanVar(value=False)

        ctk.CTkLabel(
            self,
            text="🏭 CONTROLE DE PRODUÇÃO",
            font=("Arial", 28, "bold"),
            text_color=COLOR_PRIMARY,
        ).pack(pady=20)

        self.busca = ctk.CTkEntry(
            self,
            width=500,
            placeholder_text="Pesquisar produto..."
        )
        self.busca.pack(pady=10)
        self.busca.bind("<KeyRelease>", self.filtrar)

        self.lbl_resumo = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 15, "bold")
        )

        self.lbl_resumo.pack(pady=5)

        ctk.CTkCheckBox(
            self,
            text="Mostrar somente produtos com necessidade de produção",
            variable=self.somente_faltantes,
            command=self.aplicar_filtros
        ).pack(pady=5)

        self.scroll = ctk.CTkScrollableFrame(
        self,
        fg_color="transparent"
        )

        for i in range(5):

            self.scroll.grid_columnconfigure(
                i,
                weight=1
            )

            self.scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
        
        self.frame_cards = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )

        self.frame_cards.pack(
                fill="both",
                expand=True
        )
        
        self.carregar()

    # -------------------------------------------------

    def carregar(self):

        try:

            resposta = (
                supabase
                .table("Produtos")
                .select("*")
                .eq("ativo", True)
                .eq("categoria", "PRODUCAO")
                .order("nome")
                .execute()
            )

            self.lista_produtos = resposta.data or []

            self.lista_produtos.sort(
            key=lambda p: (
                (p.get("estoque_atual") or 0)
                -
                (p.get("estoque_minimo") or 0)
            )
        )

            self.aplicar_filtros()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )

    # -------------------------------------------------

    def filtrar(self, event=None):

        self.aplicar_filtros()

# -------------------------------------------------

    def aplicar_filtros(self):

        lista = self.lista_produtos.copy()

        texto = self.busca.get().lower()

        if self.somente_faltantes.get():

            lista = [

            p for p in lista

            if (
                (p.get("estoque_atual") or 0)
                <
                (p.get("estoque_minimo") or 0)
            )
        ]

        if texto:

            lista = [

            p for p in lista

            if texto in (p.get("nome") or "").lower()
        ]

        lista.sort(

        key=lambda p:

        (
            (p.get("estoque_minimo") or 0)
            -
            (p.get("estoque_atual") or 0)
        ),

        reverse=True
    )

        self.lbl_resumo.configure(

        text=f"{len(lista)} produtos precisam de atenção"
    )

        self.renderizar(lista)

    # -------------------------------------------------

    def renderizar(self, lista):

        for w in self.frame_cards.winfo_children():
            w.destroy()

        linha = 0
        coluna = 0

        for produto in lista:

            self.criar_card(
                produto,
                linha,
                coluna
            )

            coluna += 1

            if coluna >= 5:

                coluna = 0
                linha += 1

    # -------------------------------------------------

    def criar_card(
        self,
        produto,
        linha_grid,
        coluna_grid
    ):

        nome = produto.get("nome", "")

        estoque = produto.get("estoque_atual") or 0

        estoque_minimo = produto.get("estoque_minimo") or 0

        faltam = max(
        0,
        estoque_minimo - estoque
    )

        faltam = max(
    0,
            estoque_minimo - estoque
        )

        excedente = max(
            0,
            estoque - estoque_minimo
        )

        if estoque_minimo > 0:
            percentual = min(
                estoque / estoque_minimo,
                1
            )
        else:
            percentual = 1

        percentual = min(percentual, 1)

        if faltam > 0:

            cor_card = "#ffebee"

            texto_falta = f"🔴 Produzir {faltam}"

        elif excedente > 0:

            cor_card = "#e8f5e9"

            texto_falta = f"🟢 +{excedente} acima do mínimo"

        else:

            cor_card = "#fff8e1"

            texto_falta = "🟡 Estoque no mínimo"

        card = ctk.CTkFrame(
        self.frame_cards,
        width=300,
        height=250,
        fg_color=cor_card,
        corner_radius=12,
        border_width=1
    )

        card.grid(
            row=linha_grid,
            column=coluna_grid,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        card.grid_propagate(False)

        ctk.CTkLabel(
        card,
        text=nome,
        font=("Arial", 14, "bold"),
        wraplength=250
    ).pack(
        pady=(10, 5),
        padx=10
    )

        ctk.CTkLabel(
        card,
        text=f"Atual: {estoque}"
    ).pack()

        ctk.CTkLabel(
        card,
        text=f"Mínimo: {estoque_minimo}"
    ).pack()

        ctk.CTkLabel(
        card,
        text=texto_falta,
        font=("Arial", 12, "bold")
    ).pack(
        pady=5
    )

        entrada = ctk.CTkEntry(
        card,
        width=80
    )

        entrada.pack(
        pady=5
    )

        entrada.insert(
        0,
        str(faltam)
    )

        ctk.CTkButton(
        card,
        text="+ PRODUZIR",
        fg_color=COLOR_SUCCESS,
        command=lambda p=produto, e=entrada:
        self.registrar(p, e)
    ).pack(
        pady=5
    )

        barra = ctk.CTkProgressBar(
        card,
        width=220
    )

        barra.pack(
        pady=10
    )

        barra.set(percentual)

        ctk.CTkLabel(
            card,
            text=texto_falta,
            font=("Arial", 12, "bold")
        ).pack(
            pady=(0, 10)
        )

    # -------------------------------------------------

    def registrar(self, produto, entrada):

        valor = entrada.get().strip()

        if not valor.isdigit():

            messagebox.showwarning(
                "Aviso",
                "Digite uma quantidade válida."
            )

            return

        quantidade = int(valor)

        novo_estoque = (
            (produto.get("estoque_atual") or 0)
            + quantidade
        )

        try:

            supabase.table(
                "Produtos"
            ).update({

                "estoque_atual": novo_estoque

            }).eq(

                "id",
                produto["id"]

            ).execute()

            supabase.table(
                "Historico_Producao"
            ).insert({

                "produto_id": produto["id"],
                "quantidade": quantidade,
                "data_hora": datetime.now().isoformat(),
                "usuario": "Produção",
                "observacao": f"Produzido {quantidade} un de {produto['nome']}"

            }).execute()

            messagebox.showinfo(
                "Sucesso",
                "Produção registrada."
            )

            self.carregar()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )