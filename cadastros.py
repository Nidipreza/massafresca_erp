import customtkinter as ctk


class JanelaCadastros(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Cadastros")

        self.geometry("900x600")

        ctk.CTkLabel(
            self,
            text="TELA DE CADASTROS",
            font=("Arial", 30, "bold")
        ).pack(pady=50)