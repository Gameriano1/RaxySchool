import customtkinter as ctk
import os
from main import RaxySchool


# Configurações iniciais
ctk.set_appearance_mode("dark")  # Modo escuro
ctk.set_default_color_theme("blue")  # Tema azul

# Função chamada quando o botão é clicado

invalid = False
invalid_label = None  # Variável para armazenar o rótulo de texto inválido

def open_file(event):
    # Caminho do arquivo a ser aberto
    file_path = "faltas_alunos.xlsx"
    if os.path.exists(file_path):  # Verifica se o arquivo existe
        os.startfile(file_path)  # Abre o arquivo
    else:
        print("Arquivo não encontrado!")

# Função chamada quando o botão é clicado
def on_button_click():
    global invalid, invalid_label  # Declaramos as variáveis globais
    input_text = entry.get()  # Obtém o texto do campo de entrada

    if input_text.isnumeric():
        print(f"Texto inserido: {input_text}")
        if invalid:  # Se a etiqueta de texto inválido estava visível, removemos
            invalid_label.pack_forget()
            invalid = False
        raxy = RaxySchool()
        raxy.run("NOVO", int(input_text))
        valid_label = ctk.CTkLabel(app, text="Clique aqui para ver o Relatório!!", font=("Arial", 20), text_color="Green")
        valid_label.pack(pady=20)  # Adiciona a etiqueta à janela com espaçamento vertical
        valid_label.bind("<Button-1>", open_file)


    else:
        if not invalid:  # Se o texto é inválido e a etiqueta não foi mostrada ainda
            invalid_label = ctk.CTkLabel(app, text="Texto inválido", font=("Arial", 20), text_color="red")
            invalid_label.pack(pady=20)  # Adiciona a etiqueta à janela com espaçamento vertical
            invalid = True

# Criação da janela principal
app = ctk.CTk()

app.iconbitmap('JF.ico')
app.title("Raxy School APP")  # Título da janela
app.geometry("400x300")  # Tamanho da janela

# Criação de um título
label_title = ctk.CTkLabel(app, text="Raxy School", font=("Arial", 20))
label_title.pack(pady=20)  # Adiciona o título à janela com espaçamento vertical

# Criação de um campo de entrada
entry = ctk.CTkEntry(app, width=200, placeholder_text="Fale quantos dias de faltas...")
entry.pack(pady=10)  # Adiciona o campo de entrada à janela com espaçamento vertical

# Criação de um botão
button = ctk.CTkButton(app, text="Enviar", command=on_button_click)
button.pack(pady=20)  # Adiciona o botão à janela com espaçamento vertical

# Inicia o loop da interface
app.mainloop()
