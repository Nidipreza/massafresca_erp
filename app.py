import customtkinter as ctk

from telas.menu import MenuPrincipal

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = MenuPrincipal()
app.mainloop()