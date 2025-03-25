import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import math
from datetime import datetime
import re

class CalculadoraModerna(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuração da janela principal
        self.title("Calculadora Moderna")
        self.geometry("400x600")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)
        
        # Variáveis
        self.resultado_var = tk.StringVar()
        self.expressao_atual = ""
        self.ultimo_resultado = 0
        self.historico = self.carregar_historico()
        self.modo_cientifico = False
        
        # Configuração de estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Roboto', 12), padding=5)
        self.style.configure('Numerico.TButton', background='#ffffff')
        self.style.configure('Operador.TButton', background='#e0e0e0')
        self.style.configure('Funcao.TButton', background='#d0d0d0')
        self.style.configure('Igual.TButton', background='#4caf50', foreground='white')
        self.style.configure('Limpar.TButton', background='#f44336', foreground='white')
        
        # Criar widgets
        self.criar_widgets()
        
        # Configurar atalhos de teclado
        self.bind_atalhos()
    
    def carregar_historico(self):
        """Carrega o histórico de cálculos do arquivo JSON"""
        try:
            if os.path.exists("historico.json"):
                with open("historico.json", "r") as file:
                    return json.load(file)
            return []
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
            return []
    
    def salvar_historico(self):
        """Salva o histórico de cálculos em um arquivo JSON"""
        try:
            with open("historico.json", "w") as file:
                json.dump(self.historico, file, indent=2)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o histórico: {e}")
    
    def criar_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display da calculadora
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Expressão atual (menor)
        self.expressao_label = ttk.Label(
            display_frame, 
            textvariable=tk.StringVar(value=""),
            font=("Roboto", 12),
            anchor="e"
        )
        self.expressao_label.pack(fill=tk.X)
        
        # Resultado (maior)
        resultado_entry = ttk.Entry(
            display_frame, 
            textvariable=self.resultado_var,
            font=("Roboto", 24),
            justify="right"
        )
        resultado_entry.pack(fill=tk.X, pady=5)
        
        # Abas para alternar entre calculadora normal e científica
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba da calculadora básica
        calc_basica_frame = ttk.Frame(notebook, padding=5)
        notebook.add(calc_basica_frame, text="Básica")
        
        # Aba da calculadora científica
        calc_cientifica_frame = ttk.Frame(notebook, padding=5)
        notebook.add(calc_cientifica_frame, text="Científica")
        
        # Aba do histórico
        historico_frame = ttk.Frame(notebook, padding=5)
        notebook.add(historico_frame, text="Histórico")
        
        # Configurar botões da calculadora básica
        self.configurar_calc_basica(calc_basica_frame)
        
        # Configurar botões da calculadora científica
        self.configurar_calc_cientifica(calc_cientifica_frame)
        
        # Configurar histórico
        self.configurar_historico(historico_frame)
        
        # Barra de status
        self.status_var = tk.StringVar(value="Pronto")
        status_bar = ttk.Label(self, textvariable=self.status_var, anchor=tk.W, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def configurar_calc_basica(self, parent):
        """Configura os botões da calculadora básica"""
        # Grid para os botões
        botoes_frame = ttk.Frame(parent)
        botoes_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuração dos botões
        botoes = [
            ('C', 0, 0, 'Limpar.TButton'), ('±', 0, 1, 'Funcao.TButton'), 
            ('%', 0, 2, 'Funcao.TButton'), ('÷', 0, 3, 'Operador.TButton'),
            ('7', 1, 0, 'Numerico.TButton'), ('8', 1, 1, 'Numerico.TButton'), 
            ('9', 1, 2, 'Numerico.TButton'), ('*', 1, 3, 'Operador.TButton'),
            ('4', 2, 0, 'Numerico.TButton'), ('5', 2, 1, 'Numerico.TButton'), 
            ('6', 2, 2, 'Numerico.TButton'), ('-', 2, 3, 'Operador.TButton'),
            ('1', 3, 0, 'Numerico.TButton'), ('2', 3, 1, 'Numerico.TButton'), 
            ('3', 3, 2, 'Numerico.TButton'), ('+', 3, 3, 'Operador.TButton'),
            ('0', 4, 0, 'Numerico.TButton', 2), ('.', 4, 2, 'Numerico.TButton'), 
            ('=', 4, 3, 'Igual.TButton')
        ]
        
        # Criar botões
        for botao in botoes:
            if len(botao) == 5:  # Botão com colspan
                texto, linha, coluna, estilo, colspan = botao
                btn = ttk.Button(
                    botoes_frame, 
                    text=texto, 
                    style=estilo,
                    command=lambda t=texto: self.processar_botao(t)
                )
                btn.grid(row=linha, column=coluna, columnspan=colspan, padx=2, pady=2, sticky="nsew")
            else:
                texto, linha, coluna, estilo = botao
                btn = ttk.Button(
                    botoes_frame, 
                    text=texto, 
                    style=estilo,
                    command=lambda t=texto: self.processar_botao(t)
                )
                btn.grid(row=linha, column=coluna, padx=2, pady=2, sticky="nsew")
        
        # Configurar o redimensionamento das linhas e colunas
        for i in range(5):
            botoes_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            botoes_frame.grid_columnconfigure(i, weight=1)
    
    def configurar_calc_cientifica(self, parent):
        """Configura os botões da calculadora científica"""
        # Grid para os botões
        botoes_frame = ttk.Frame(parent)
        botoes_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuração dos botões científicos
        botoes = [
            ('sin', 0, 0, 'Funcao.TButton'), ('cos', 0, 1, 'Funcao.TButton'), 
            ('tan', 0, 2, 'Funcao.TButton'), ('log', 0, 3, 'Funcao.TButton'),
            ('ln', 1, 0, 'Funcao.TButton'), ('x²', 1, 1, 'Funcao.TButton'), 
            ('x³', 1, 2, 'Funcao.TButton'), ('xʸ', 1, 3, 'Funcao.TButton'),
            ('√', 2, 0, 'Funcao.TButton'), ('∛', 2, 1, 'Funcao.TButton'), 
            ('π', 2, 2, 'Funcao.TButton'), ('e', 2, 3, 'Funcao.TButton'),
            ('(', 3, 0, 'Funcao.TButton'), (')', 3, 1, 'Funcao.TButton'), 
            ('mod', 3, 2, 'Funcao.TButton'), ('1/x', 3, 3, 'Funcao.TButton'),
            ('MC', 4, 0, 'Funcao.TButton'), ('MR', 4, 1, 'Funcao.TButton'), 
            ('M+', 4, 2, 'Funcao.TButton'), ('M-', 4, 3, 'Funcao.TButton')
        ]
        
        # Criar botões
        for texto, linha, coluna, estilo in botoes:
            btn = ttk.Button(
                botoes_frame, 
                text=texto, 
                style=estilo,
                command=lambda t=texto: self.processar_botao_cientifico(t)
            )
            btn.grid(row=linha, column=coluna, padx=2, pady=2, sticky="nsew")
        
        # Configurar o redimensionamento das linhas e colunas
        for i in range(5):
            botoes_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            botoes_frame.grid_columnconfigure(i, weight=1)
    
    def configurar_historico(self, parent):
        """Configura a aba de histórico"""
        # Frame para o histórico
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Listbox para exibir o histórico
        self.historico_listbox = tk.Listbox(
            frame, 
            font=("Roboto", 12),
            height=15
        )
        self.historico_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar para o histórico
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.historico_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.historico_listbox.config(yscrollcommand=scrollbar.set)
        
        # Botões para gerenciar o histórico
        botoes_frame = ttk.Frame(parent)
        botoes_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            botoes_frame, 
            text="Limpar Histórico", 
            command=self.limpar_historico
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            botoes_frame, 
            text="Usar Selecionado", 
            command=self.usar_historico_selecionado
        ).pack(side=tk.RIGHT, padx=5)
        
        # Preencher o histórico
        self.atualizar_historico_listbox()
    
    def atualizar_historico_listbox(self):
        """Atualiza a listbox com os itens do histórico"""
        self.historico_listbox.delete(0, tk.END)
        for item in self.historico:
            self.historico_listbox.insert(tk.END, f"{item['expressao']} = {item['resultado']}")
    
    def limpar_historico(self):
        """Limpa todo o histórico"""
        if messagebox.askyesno("Limpar Histórico", "Tem certeza que deseja limpar todo o histórico?"):
            self.historico = []
            self.salvar_historico()
            self.atualizar_historico_listbox()
            self.status_var.set("Histórico limpo")
    
    def usar_historico_selecionado(self):
        """Usa o item selecionado no histórico"""
        try:
            indice = self.historico_listbox.curselection()[0]
            item = self.historico[indice]
            self.resultado_var.set(str(item['resultado']))
            self.expressao_atual = str(item['resultado'])
            self.expressao_label.config(text=item['expressao'])
            self.status_var.set(f"Valor carregado do histórico: {item['resultado']}")
        except IndexError:
            messagebox.showinfo("Aviso", "Selecione um item do histórico primeiro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível usar o item selecionado: {e}")
    
    def bind_atalhos(self):
        """Configura os atalhos de teclado"""
        # Números e operações básicas
        for i in range(10):
            self.bind(str(i), lambda e, digit=i: self.processar_botao(str(digit)))
        
        self.bind('+', lambda e: self.processar_botao('+'))
        self.bind('-', lambda e: self.processar_botao('-'))
        self.bind('*', lambda e: self.processar_botao('×'))
        self.bind('/', lambda e: self.processar_botao('÷'))
        self.bind('.', lambda e: self.processar_botao('.'))
        self.bind('<Return>', lambda e: self.processar_botao('='))
        self.bind('<BackSpace>', lambda e: self.apagar_ultimo_caractere())
        self.bind('<Escape>', lambda e: self.processar_botao('C'))
        
        # Teclas científicas
        self.bind('(', lambda e: self.processar_botao_cientifico('('))
        self.bind(')', lambda e: self.processar_botao_cientifico(')'))
        self.bind('^', lambda e: self.processar_botao_cientifico('xʸ'))
    
    def apagar_ultimo_caractere(self):
        """Apaga o último caractere da expressão atual"""
        if self.expressao_atual:
            self.expressao_atual = self.expressao_atual[:-1]
            self.resultado_var.set(self.expressao_atual)
            self.status_var.set("Caractere apagado")
    
    def processar_botao(self, valor):
        """Processa o clique em um botão da calculadora básica"""
        if valor == 'C':
            self.resultado_var.set("")
            self.expressao_atual = ""
            self.status_var.set("Limpar")
        elif valor == '=':
            try:
                resultado = eval(self.resultado_var.get())
                self.historico.append({"expressao": self.resultado_var.get(), "resultado": resultado})
                self.salvar_historico()
                self.resultado_var.set(str(resultado))
                self.expressao_atual = str(resultado)
                self.status_var.set("Resultado calculado")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        elif valor == '%':
            try:
                valores = self.resultado_var.get().split()
                if len(valores) == 2:
                    x = float(valores[0])
                    y = float(valores[1])
                    resultado = (x / 100) * y
                    self.historico.append({"expressao": f"{x} % de {y}", "resultado": resultado})
                    self.salvar_historico()
                    self.resultado_var.set(str(resultado))
                    self.expressao_atual = str(resultado)
                    self.status_var.set("Porcentagem calculada")
                else:
                    messagebox.showerror("Erro", "Insira dois valores válidos para calcular a porcentagem.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            self.resultado_var.set(self.resultado_var.get() + valor)
            self.expressao_atual += valor
            self.status_var.set("Valor adicionado")
    
    def processar_botao_cientifico(self, valor):
        """Processa o clique em um botão da calculadora científica"""
        if valor == 'C':
            self.resultado_var.set("")
            self.expressao_atual = ""
            self.status_var.set("Limpar")
        elif valor == '=':
            try:
                resultado = eval(self.resultado_var.get())
                self.historico.append({"expressao": self.resultado_var.get(), "resultado": resultado})
                self.salvar_historico()
                self.resultado_var.set(str(resultado))
                self.expressao_atual = str(resultado)
                self.status_var.set("Resultado calculado")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        elif valor == '%':
            try:
                valores = self.resultado_var.get().split()
                if len(valores) == 2:
                    x = float(valores[0])
                    y = float(valores[1])
                    resultado = (x / 100) * y
                    self.historico.append({"expressao": f"{x} % de {y}", "resultado": resultado})
                    self.salvar_historico()
                    self.resultado_var.set(str(resultado))
                    self.expressao_atual = str(resultado)
                    self.status_var.set("Porcentagem calculada")
                else:
                    messagebox.showerror("Erro", "Insira dois valores válidos para calcular a porcentagem.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            self.resultado_var.set(self.resultado_var.get() + valor)
            self.expressao_atual += valor
            self.status_var.set("Valor adicionado")
if __name__ == "__main__":
    app = CalculadoraModerna()
    app.mainloop()
