import customtkinter as ctk


class JanelaExpedicao(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Expedição")

        self.geometry("900x600")

        ctk.CTkLabel(
            self,
            text="TELA DE EXPEDIÇÃO",
            font=("Arial", 30, "bold")
        ).pack(pady=50)