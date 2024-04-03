import embed_api as api

import time
import tkinter as tk
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk

class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        api.configurar()    # Configuração da API
        api.iniciar()       # Inicialização do produto POS

        # Variáveis de cores
        self.cor_fundo = "black"
        self.cor_botao = "green"
        self.cor_texto = "white"

        self.title("Embed")
        self.overrideredirect(False)  # Mostra a barra de título

        # Responsividade
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)  # Ocupa 4/5 da tela
        self.grid_columnconfigure(0, weight=1)

        self.header = HeaderFrame(self, bg=self.cor_fundo)
        self.header.grid(row=0, column=0, sticky="nsew")

        self.content = ContentFrame(self, bg=self.cor_fundo)
        self.content.grid(row=1, column=0, sticky="nsew")

        self.frames = {
            "TelaPrincipal": TelaPrincipal, 
            "TelaDebito": TelaDebito, 
            "TelaCredito": TelaCredito,
            "TelaProcessamento": TelaProcessamento,
        }
        self.mostrar_frame("TelaPrincipal")

    def mostrar_frame(self, page_name):
        frame_class = self.frames[page_name]
        self.content.mostrar_frame(frame_class)

class HeaderFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.current_logo_index = 0
        self.logos = [
            Image.open("img/logo1.png"), 
            Image.open("img/logo2.png"),
            Image.open("img/logo3.png"),
        ]

        self.logo_photo = ImageTk.PhotoImage(self.logos[self.current_logo_index])
        self.logo_label = tk.Label(self, image=self.logo_photo)
        self.logo_label.pack(pady=1)

        # Alterna entre as imagens do logo a cada segundo
        self.after(1000, self.toggle_logo)

    def toggle_logo(self):
        self.current_logo_index = (self.current_logo_index + 1) % len(self.logos)
        self.logo_photo = ImageTk.PhotoImage(self.logos[self.current_logo_index])
        self.logo_label.config(image=self.logo_photo)
        self.after(1000, self.toggle_logo)

class ContentFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.controller = None  # Será atribuído na chamada de mostrar_frame

    def mostrar_frame(self, frame_class):
        if self.controller:
            self.controller.destroy()

        self.controller = frame_class(self)
        self.controller.pack(fill="both", expand=True)

class TelaPrincipal(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent.master.cor_fundo)
        self.parent = parent
        
        self.label = tk.Label(self, text="Formas de pagamento\n", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 32))
        self.label.pack()

        self.debito_button = tk.Button(self, text="Débito", command=lambda: self.parent.master.mostrar_frame("TelaDebito"), height=5, width=20, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 12, 'bold'))
        self.debito_button.pack(pady=10)

        self.credito_button = tk.Button(self, text="Crédito", command=lambda: self.parent.master.mostrar_frame("TelaCredito"),  height=5, width=20, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 12, 'bold'))
        self.credito_button.pack(pady=10)

class TelaDebito(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent.master.cor_fundo)
        self.parent = parent

        self.label = tk.Label(self, text="Valor do débito:", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 26))
        self.label.pack()

        self.textbox = tk.Entry(self, font=('Helvetica', 18))
        self.textbox.pack(pady=10)

        self.button_frame = tk.Frame(self, bg=self.parent.master.cor_fundo)
        self.button_frame.pack(padx=30)

        self.ok_button = tk.Button(self.button_frame, text="OK", command=self.processar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.ok_button.pack(side="left", padx=10)

        self.voltar_button = tk.Button(self.button_frame, text="Voltar", command=self.voltar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.voltar_button.pack(pady=10)

    def processar(self):
        valor = self.textbox.get()
        print("Valor do débito:", valor)

        result = api.debito(valor)
        if result == "1":
            self.parent.master.mostrar_frame("TelaProcessamento")

    def voltar(self):
        self.parent.master.mostrar_frame("TelaPrincipal")

class TelaCredito(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent.master.cor_fundo)
        self.parent = parent

        self.label1 = tk.Label(self, text="Valor do crédito:", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 26))
        self.label1.pack()

        self.textbox1 = tk.Entry(self, font=('Helvetica', 18))
        self.textbox1.pack(pady=10)

        self.label2 = tk.Label(self, text="Quantidade de parcelas:", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 26))
        self.label2.pack()

        self.textbox2 = tk.Entry(self, font=('Helvetica', 18))
        self.textbox2.pack(pady=10)

        self.button_frame = tk.Frame(self, bg=self.parent.master.cor_fundo)
        self.button_frame.pack(padx=20)

        self.ok_button = tk.Button(self.button_frame, text="OK", command=self.processar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.ok_button.pack(side="left", padx=10)

        self.voltar_button = tk.Button(self.button_frame, text="Voltar", command=self.voltar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.voltar_button.pack(pady=10)

    def processar(self):
        valor = self.textbox1.get()
        parcelas = self.textbox2.get()
        
        result = api.credito(valor, parcelas)
        if result == "1":
            self.parent.master.mostrar_frame("TelaProcessamento")

    def voltar(self):
        self.parent.master.mostrar_frame("TelaPrincipal")

class TelaProcessamento(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent.master.cor_fundo)
        self.parent = parent

        self.label = tk.Label(self, text="Verifique o pedido de pagamento no dispositivo Android", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.label.pack(pady=10)

        self.spinner = ttk.Progressbar(self, mode='indeterminate', )
        self.spinner.pack(pady=10)
        self.spinner.start()

        self.status_label = tk.Label(self, text="Aguardando pagamento...", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.status_label.pack(pady=10)

        self.button_frame = tk.Frame(self, bg=self.parent.master.cor_fundo)
        self.button_frame.pack(padx=20)

        self.cancel_button = tk.Button(self.button_frame, text="Cancelar", command=self.cancelar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.cancel_button.pack(side="left", padx=10)

        self.voltar_button = tk.Button(self.button_frame, text="Voltar", command=self.voltar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.voltar_button.pack(pady=10)

        self.process_thread = Thread(target=self.processar)
        self.process_thread.start()    
        
    def processar(self):
        while True:
            result = api.status()
            if result == "0":
                api.finalizar()

                self.label.pack_forget()
                self.spinner.pack_forget()
                self.button_frame.pack_forget()
                self.status_label.config(text="Pagamento confirmado!", font=('Helvetica', 26))

                time.sleep(3)
                self.voltar()
                break

    def cancelar(self):
        print("Cancelando operação")

    def voltar(self):
        self.parent.master.mostrar_frame("TelaPrincipal")

if __name__ == "__main__":
    app = Main()
    app.mainloop()
