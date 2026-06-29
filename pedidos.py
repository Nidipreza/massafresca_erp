import customtkinter as ctk
import tkinter.messagebox as messagebox
from datetime import datetime

from conexao import supabase

from config import (
    COLOR_PRIMARY,
    COLOR_SUCCESS,
    COLOR_BG_APP
)


class JanelaPedido(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Pedidos")

        self.after(0, lambda: self.state("zoomed"))

        self.configure(
            fg_color=COLOR_BG_APP
        )

        self.grab_set()

        self.clientes = []
        self.produtos = []

        self.itens = []

        titulo = ctk.CTkLabel(
            self,
            text="📦 NOVO PEDIDO",
            font=("Arial", 28, "bold"),
            text_color=COLOR_PRIMARY
        )

        titulo.pack(
            pady=20
        )

        self.carregar_clientes()
        print("CLIENTES OK")

        self.carregar_produtos()
        print("PRODUTOS OK")

        frame_topo = ctk.CTkFrame(self)

        for i in range(8):

            frame_topo.grid_columnconfigure(
                i,
                weight=1
            )

        frame_topo.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkLabel(
            frame_topo,
            text="Cliente"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.combo_cliente = ctk.CTkComboBox(
        frame_topo,
        values=self.clientes,
        width=250
        )

        self.combo_cliente.set("")

        self.combo_cliente.grid(
            row=0,
            column=1,
            padx=10
        )

        ctk.CTkLabel(
            frame_topo,
            text="Data Entrega"
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        self.data_entrega = ctk.CTkEntry(
            frame_topo,
            width=150
        )

        self.data_entrega.grid(
            row=0,
            column=3,
            padx=10
        )

        self.data_entrega.insert(
            0,
            datetime.now().strftime("%d/%m/%Y")
        )

        ctk.CTkLabel(
            frame_topo,
            text="NF"
        ).grid(
            row=0,
            column=4,
            padx=10,
            pady=10
        )

        self.nf = ctk.CTkEntry(
            frame_topo,
            width=200
        )

        self.nf.grid(
            row=0,
            column=5,
            padx=10
        )

        ctk.CTkLabel(
            frame_topo,
            text="Nº Caixas"
        ).grid(
            row=0,
            column=6,
            padx=10
        )

        self.numero_caixas = ctk.CTkEntry(
            frame_topo,
            width=120
        )

        self.numero_caixas.grid(
            row=0,
            column=7,
            padx=10
        )

        ctk.CTkLabel(
            frame_topo,
            text="Motorista"
        ).grid(
            row=1,
            column=0,
            padx=10
        )

        self.motorista = ctk.CTkEntry(
            frame_topo,
            width=250
        )

        self.motorista.grid(
            row=1,
            column=1,
            padx=10
        )

        ctk.CTkLabel(
            frame_topo,
            text="Veículo"
        ).grid(
            row=1,
            column=2,
            padx=10,
            pady=10
        )

        self.veiculo = ctk.CTkEntry(
            frame_topo,
            width=200
        )

        self.veiculo.grid(
            row=1,
            column=3,
            padx=10
        )

        frame_itens = ctk.CTkFrame(self)

        frame_itens.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkLabel(
            frame_itens,
            text="Produto"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.combo_produto = ctk.CTkComboBox(
            frame_itens,
            width=350,
            values=self.produtos
        )

        self.combo_produto.set("")

        self.combo_produto.grid(
            row=0,
            column=1,
            padx=10
        )

        ctk.CTkLabel(
            frame_itens,
            text="Quantidade"
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        self.qtd = ctk.CTkEntry(
            frame_itens,
            width=100
        )

        self.qtd.grid(
            row=0,
            column=3,
            padx=10
        )

        ctk.CTkButton(
            frame_itens,
            text="+ Adicionar",
            command=self.adicionar_item
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        self.lista_itens = ctk.CTkScrollableFrame(
        self,
        height=250
        )

        self.lista_itens.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.lista_itens.pack(
            fill="both",
            padx=20,
            pady=10
        )


        print("CRIANDO RODAPE")

# =====================================================
# RODAPÉ
# =====================================================

        frame_rodape = ctk.CTkFrame(
            self,
            height=70
        )

        frame_rodape.pack(
            fill="x",
            padx=20,
            pady=(5,10)
        )

        self.lbl_total = ctk.CTkLabel(
            frame_rodape,
            text="Total itens: 0",
            font=("Arial", 16, "bold")
        )

        self.lbl_total.pack(
            side="left",
            padx=20
        )

        ctk.CTkButton(
            frame_rodape,
            text="🧹 LIMPAR",
            width=120,
            fg_color="#616161",
            command=self.limpar_tela
        ).pack(
            side="right",
            padx=5
        )

        ctk.CTkButton(
            frame_rodape,
            text="📋 CLONAR",
            width=120,
            fg_color="#6a1b9a",
            command=self.clonar_pedido
        ).pack(
            side="right",
            padx=5
        )

        ctk.CTkButton(
            frame_rodape,
            text="💾 SALVAR PEDIDO",
            width=180,
            fg_color="#2e7d32",
            command=self.salvar_pedido
        ).pack(
            side="right",
            padx=5
        )

        ctk.CTkLabel(
            self,
            text="Observações"
        ).pack()

        self.observacao = ctk.CTkTextbox(
            self,
            height=60
        )

        self.observacao.pack(
            fill="x",
            padx=20,
            pady=10
        )



# =====================================================

    def carregar_clientes(self):

        resposta = (
            supabase
            .table("Clientes")
            .select("*")
            .order("nome_fantasia")
            .execute()
        )

        self.clientes = [
            c["nome_fantasia"]
            for c in resposta.data
        ]
# =====================================================
    def carregar_produtos(self):

        resposta = (
            supabase
            .table("Produtos")
            .select("*")
            .eq("ativo", True)
            .order("nome")
            .execute()
        )

        self.produtos_db = resposta.data

        self.produtos = [""]

        self.produtos.extend(
            [
                p["nome"]
                for p in resposta.data
            ]
        )


# =====================================================
    def adicionar_item(self):

        produto = self.combo_produto.get()

        qtd = self.qtd.get()

        produto = self.combo_produto.get()

        if produto == "":

            messagebox.showwarning(
                "Aviso",
                "Selecione um produto."
            )

            return

        if not qtd.isdigit():

            messagebox.showwarning(
                "Aviso",
                "Quantidade inválida."
            )

            return

        self.itens.append({
            "produto": produto,
            "quantidade": int(qtd)
        })

        self.atualizar_lista()

        self.qtd.delete(0, "end")


# -------------------------------------------------------------------------
    def clonar_pedido(self):

        messagebox.showinfo(
            "Em desenvolvimento",
            "Clonar pedido será a próxima etapa."
        )
# -------------------------------------------------------------------------

    def atualizar_lista(self):

        for w in self.lista_itens.winfo_children():
            w.destroy()

        total = 0

        for indice, item in enumerate(self.itens):

            linha = ctk.CTkFrame(
                self.lista_itens,
                fg_color="transparent"
            )

            linha.pack(
                fill="x",
                pady=3,
                padx=5
            )

            ctk.CTkLabel(
            linha,
            text=item["produto"],
            width=300,
            anchor="w"
        ).pack(
            side="left",
            padx=10
        )

        controle = ctk.CTkFrame(
            linha,
            fg_color="transparent"
        )

        controle.pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            controle,
            text="-",
            width=28,
            command=lambda i=indice: self.diminuir_qtd(i)
        ).pack(side="left")

        qtd = ctk.CTkEntry(
            controle,
            width=50,
            justify="center"
        )

        qtd.insert(
            0,
            str(item["quantidade"])
        )

        qtd.pack(
            side="left",
            padx=2
        )

        item["entry"] = qtd

        qtd.bind(
            "<KeyRelease>",
            lambda e: self.calcular_total()
        )

        ctk.CTkButton(
            controle,
            text="+",
            width=28,
            command=lambda i=indice: self.aumentar_qtd(i)
        ).pack(side="left")

        ctk.CTkButton(
            linha,
            text="🗑",
            width=40,
            fg_color="#c62828",
            command=lambda i=indice: self.excluir_item(i)
        ).pack(
            side="right",
            padx=5
        )

        self.calcular_total()

  # -------------------------------------------------------------------------


    def aumentar_qtd(self, indice):

        item = self.itens[indice]

        valor = int(item["entry"].get())

        valor += 1

        item["entry"].delete(0, "end")

        item["entry"].insert(0, str(valor))

        self.calcular_total()

# -------------------------------------------------------------------------

    def diminuir_qtd(self, indice):

        item = self.itens[indice]

        valor = int(item["entry"].get())

        if valor > 1:

            valor -= 1

            item["entry"].delete(0, "end")

            item["entry"].insert(0, str(valor))

        self.calcular_total()

  # -------------------------------------------------------------------------

    def calcular_total(self):

        total = 0

        for item in self.itens:

            try:

                total += int(
                    item["entry"].get()
                )

            except:

                pass

        self.lbl_total.configure(
            text=f"Total itens: {total}"
        )

# -------------------------------------------------------------------------

    def editar_item_inline(self, indice):

        item = self.itens[indice]

        self.combo_produto.set(
            item["produto"]
        )

        self.qtd.delete(0, "end")

        self.qtd.insert(
            0,
            str(item["quantidade"])
        )

        self.itens.pop(indice)

        self.atualizar_lista()

 # -------------------------------------------------------------------------

    def editar_item(self, indice):

        item = self.itens[indice]

        janela = ctk.CTkToplevel(self)

        janela.title("Editar Item")

        janela.geometry("350x220")

        ctk.CTkLabel(
            janela,
            text=item["produto"],
            font=("Arial", 16, "bold")
        ).pack(
            pady=15
        )

        entrada = ctk.CTkEntry(
            janela,
            width=120
        )

        entrada.pack(
            pady=10
        )

        entrada.insert(
            0,
            str(item["quantidade"])
        )

        def salvar():

            valor = entrada.get()

            if not valor.isdigit():

                messagebox.showwarning(
                    "Aviso",
                    "Quantidade inválida."
                )

                return

            self.itens[indice]["quantidade"] = int(valor)

            self.atualizar_lista()

            janela.destroy()

        ctk.CTkButton(
            janela,
            text="Salvar",
            command=salvar
        ).pack(
            pady=20
        )

# -------------------------------------------------------------------------
    def excluir_item(self, indice):

        del self.itens[indice]

        self.atualizar_lista()

# -------------------------------------------------------------------------

    def salvar_pedido(self):

# Atualiza as quantidades digitadas na tela

        for item in self.itens:

            try:

                item["quantidade"] = int(
                    item["entry"].get()
                )

            except:

                messagebox.showwarning(
                    "Aviso",
                    f"Quantidade inválida para {item['produto']}"
                )

                return

        for item in self.itens:

            item["quantidade"] = int(
            item["entry"].get()
        )

        if self.combo_cliente.get() == "":

            messagebox.showwarning(
                "Aviso",
                "Selecione um cliente."
            )

            return

        if len(self.itens) == 0:

            messagebox.showwarning(
                "Aviso",
                "Adicione itens ao pedido."
            )

            return

        erros_estoque = []

        for item in self.itens:

            produto_db = next(

                (
                    p
                    for p in self.produtos_db
                    if p["nome"] == item["produto"]
                ),

                None

            )

            if not produto_db:
                continue

            estoque = produto_db.get(
                "estoque_atual",
                0
            )

            if estoque < item["quantidade"]:

                erros_estoque.append(

                    f"{item['produto']}\n"
                    f"Disponível: {estoque}\n"
                    f"Pedido: {item['quantidade']}"

                )

        if erros_estoque:

            messagebox.showerror(
                "Estoque insuficiente",
                "\n\n".join(erros_estoque)
            )

            return

        try:

            cliente_nome = self.combo_cliente.get()

            pedido = (

                supabase
                .table("Pedidos")
              .insert({

                "cliente_nome": cliente_nome,

                "nf": self.nf.get(),

                "motorista": self.motorista.get(),

                "veiculo": self.veiculo.get(),

                "numero_caixas": self.numero_caixas.get(),

                "observacao": self.observacao.get(
                    "1.0",
                    "end"
                ),

                "data_pedido": datetime.now().isoformat(),

                "data_entrega": self.data_entrega.get(),

                "status": "ABERTO"

            })
                .execute()

            )

            pedido_id = pedido.data[0]["id"]

            for item in self.itens:

                produto_db = next(

                    (
                        p
                        for p in self.produtos_db
                        if p["nome"] == item["produto"]
                    ),

                    None

                )

                if not produto_db:
                    continue

                quantidade = item["quantidade"]

                supabase.table(
                    "Itens_Pedido"
                ).insert({

                    "pedido_id": pedido_id,
                    "produto_id": produto_db["id"],
                    "produto_nome": produto_db["nome"],
                    "quantidade": quantidade

                }).execute()

                novo_estoque = (

                    produto_db["estoque_atual"]
                    - quantidade

                )

                supabase.table(
                    "Produtos"
                ).update({

                    "estoque_atual": novo_estoque

                }).eq(

                    "id",
                    produto_db["id"]

                ).execute()

                supabase.table(
                    "Movimentacao_Estoque"
                ).insert({

                    "produto_id": produto_db["id"],
                    "tipo": "SAIDA_PEDIDO",
                    "quantidade": quantidade,
                    "data_hora": datetime.now().isoformat(),
                    "observacao":
                        f"Pedido #{pedido_id} - {cliente_nome}"

                }).execute()

            messagebox.showinfo(
                "Sucesso",
                f"Pedido #{pedido_id} criado."
            )

            self.limpar_tela()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )

 # -------------------------------------------------------------------------

    def limpar_tela(self):

        self.itens.clear()

        self.atualizar_lista()

        self.lbl_total.configure(
            text="Total itens: 0"
        )

        self.combo_cliente.set("")

        self.combo_produto.set("")

        self.qtd.delete(0, "end")
        self.qtd.insert(0, "1")

        self.nf.delete(0, "end")

        self.motorista.delete(0, "end")

        self.veiculo.delete(0, "end")

        self.numero_caixas.delete(0, "end")

        self.observacao.delete(
            "1.0",
            "end"
        )
 # -------------------------------------------------------------------------
    def remover_item(self):

        valor = self.txt_remover.get().strip()

        if not valor.isdigit():
            return

        indice = int(valor)

        if indice >= len(self.itens):
            return

        del self.itens[indice]

        self.atualizar_lista()

        self.txt_remover.delete(
            0,
            "end"
        )