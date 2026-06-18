import os

import requests
from cryptography.fernet import Fernet
import customtkinter as ctk

# Nome do arquivo para armazenar os dados
FILENAME = "itens/extras/login_data.enc"

# Gera uma chave para criptografia ou carrega a existente
def generate_key():
    key_file = "itens/extras/secret.key"
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as keyfile:
            keyfile.write(key)
    else:
        with open(key_file, "rb") as keyfile:
            key = keyfile.read()
    return key

# Função para criptografar e salvar login, senha e número
def save_credentials(login, password, number):
    key = generate_key()
    fernet = Fernet(key)

    decrypted_data = f"{login}:{password}:{number}"

    encrypted_data = fernet.encrypt(decrypted_data.encode())

    with open(FILENAME, "wb") as file:
        file.write(encrypted_data)
    print("Credenciais salvas com sucesso!")

# Função para carregar e descriptografar credenciais
def load_credentials():
    if not os.path.exists(FILENAME):
        print("Arquivo de credenciais não encontrado.")
        return

    key = generate_key()
    fernet = Fernet(key)

    with open(FILENAME, "rb") as file:
        encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data).decode()

    return decrypted_data.split(":")

# Função para mostrar a janela de cadastro
def show_registration_window():
    global user_credentials  # Declarar como global no início

    def register_and_proceed():
        login = login_entry.get()
        password = password_entry.get()
        number = number_entry.get()

        # Validação para garantir que todos os campos estejam preenchidos
        if not login or not password or not number:
            error_label.configure(text="Todos os campos são obrigatórios!")
            return
        if not number.isdigit():
            error_label.configure(text="Digite um número válido!")
            return

        # Faz a requisição
        itens = requests.post('https://sed.educacao.sp.gov.br/Logon/LogOn/', data=f'usuario={login}&senha={password}',
                              headers={
                                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
                                  'Referer': 'https://frequencia.sed.educacao.sp.gov.br/Frequencia/Index'
                              }).json()

        # Verifica se a requisição foi bem-sucedida
        if isinstance(itens, list):
            save_credentials(login, password, number)
            user_credentials = (login, password, number)  # Armazena as credenciais para retornar
            registration_window.destroy()
        else:
            error_label.configure(text="Login Inválido!")
            return

    def on_close():
        # Se a janela for fechada sem cadastrar, encerra o programa
        if user_credentials is None:
            exit()

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("themes/violet.json")

    registration_window = ctk.CTk()
    registration_window.title("Cadastro")
    registration_window.geometry("500x550")
    registration_window.attributes("-topmost", True)  # Fica 'ontop'

    # Define ação ao fechar a janela
    registration_window.protocol("WM_DELETE_WINDOW", on_close)

    ctk.CTkLabel(registration_window, text="Cadastro", font=("Cascadia Mono", 50)).pack(pady=30)

    ctk.CTkLabel(registration_window, text="Cadastro de Login", font=("Cascadia Mono", 18)).pack(pady=10)
    login_entry = ctk.CTkEntry(registration_window, font=("Cascadia Mono", 13))
    login_entry.pack(pady=5)

    ctk.CTkLabel(registration_window, text="Senha", font=("Cascadia Mono", 18)).pack(pady=10)
    password_entry = ctk.CTkEntry(registration_window, show="*", font=("Cascadia Mono", 13))
    password_entry.pack(pady=5)

    ctk.CTkLabel(registration_window, text="Número (Telefone)", font=("Cascadia Mono", 18)).pack(pady=10)
    number_entry = ctk.CTkEntry(registration_window, font=("Cascadia Mono", 13))
    number_entry.pack(pady=5)

    register_button = ctk.CTkButton(registration_window, text="Cadastrar", command=register_and_proceed,
                                    font=("Cascadia Mono", 18), width=50, height=40)
    register_button.pack(pady=40)

    error_label = ctk.CTkLabel(registration_window, text="", font=("Cascadia Mono", 18))
    error_label.pack()

    registration_window.mainloop()

# Início do programa
def login():
    global user_credentials  # Declarar como global no início da função
    user_credentials = None

    if not os.path.isfile(FILENAME):
        # Abre a janela de cadastro para novo usuário
        show_registration_window()

    # Após o cadastro, carrega e descriptografa as credenciais
    if user_credentials is None:
        user_credentials = load_credentials()

    return user_credentials

if __name__ == "__main__":
    credentials = login()
    if credentials:
        print(f"Credenciais descriptografadas: {credentials}")
