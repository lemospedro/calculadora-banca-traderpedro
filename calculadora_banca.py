import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Plataforma de Sinais")
        self.root.geometry("500x300")
        
        # Definindo a variável de tema
        self.is_dark_mode = False

        # Alterando o fundo e a cor de texto com base no tema
        self.change_theme()

        # Título da plataforma
        self.title_label = tk.Label(self.root, text="Plataforma de Sinais", font=("Arial", 24), pady=20)
        self.title_label.pack()

        # Descrição
        self.description_label = tk.Label(self.root, text="Aqui você verá os sinais de compra e venda", font=("Arial", 12))
        self.description_label.pack()

        # Botão de modo claro/escuro
        self.toggle_theme_button = tk.Button(self.root, text="Modo Claro", command=self.toggle_theme, font=("Arial", 12))
        self.toggle_theme_button.pack(pady=10)

        # Status de sinal
        self.signal_label = tk.Label(self.root, text="Buscando Sinal...", font=("Arial", 16), bg=self.bg_color, fg=self.fg_color)
        self.signal_label.pack(pady=20)

        # Simulando um sinal de compra ou venda
        self.toggle_signal_button = tk.Button(self.root, text="Simular Sinal", command=self.toggle_signal, font=("Arial", 12))
        self.toggle_signal_button.pack(pady=10)

    def change_theme(self):
        """Muda o tema para claro ou escuro"""
        if self.is_dark_mode:
            self.bg_color = "#333333"
            self.fg_color = "#FFFFFF"
        else:
            self.bg_color = "#FFFFFF"
            self.fg_color = "#000000"

        self.root.config(bg=self.bg_color)
        self.title_label.config(bg=self.bg_color, fg=self.fg_color)
        self.description_label.config(bg=self.bg_color, fg=self.fg_color)
        self.toggle_theme_button.config(bg=self.bg_color, fg=self.fg_color)
        self.signal_label.config(bg=self.bg_color, fg=self.fg_color)
        self.toggle_signal_button.config(bg=self.bg_color, fg=self.fg_color)

    def toggle_theme(self):
        """Alterna entre modo claro e escuro"""
        self.is_dark_mode = not self.is_dark_mode
        self.change_theme()

        # Atualiza o texto do botão
        if self.is_dark_mode:
            self.toggle_theme_button.config(text="Modo Claro")
        else:
            self.toggle_theme_button.config(text="Modo Escuro")

    def toggle_signal(self):
        """Simula a troca de sinal"""
        current_text = self.signal_label.cget("text")
        if current_text == "Buscando Sinal...":
            self.signal_label.config(text="Sinal Detectado: Compra", fg="green")
        else:
            self.signal_label.config(text="Buscando Sinal...", fg=self.fg_color)

# Criação da janela principal
root = tk.Tk()
app = App(root)

# Inicia a interface gráfica
root.mainloop()
