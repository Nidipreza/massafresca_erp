def carregar(self):

    for w in self.frame_lista.winfo_children():
        w.destroy()

    # aqui vamos montar o planejamento automático

    ctk.CTkLabel(

        self.frame_lista,

        text="Em desenvolvimento..."

    ).pack(pady=20)