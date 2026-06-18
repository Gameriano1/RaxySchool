
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from itens.MENSAGEM_EM_MASSA.mensagem_em_massa import MassMessageApp
from itens.AlunoPresente import UI
from itens import extras


class MenuApp:
    def __init__(self,usuario, senha, numero_telefone):

        self.app = None
        self.logo_label = None
        self.botao_opcao_1 = None
        self.botao_opcao_2 = None
        self.botao_opcao_3 = None
        self.numero_telefone = numero_telefone  # Para armazenar o número de telefone
        self.login = usuario  # Definir login de exemplo
        self.senha = senha  # Definir senha de exemplo

    # Funções das opções

    def opcao_1(self):
        self.botao_opcao_1.configure(state="disabled")
        self.botao_opcao_2.configure(state="disabled")
        self.botao_opcao_3.configure(state="disabled")

        aplicativo = UI.JFapp(self.numero_telefone, self.app)
        aplicativo.main()

        def habilitar_botoes():
            self.botao_opcao_1.configure(state="normal")
            self.botao_opcao_2.configure(state="normal")
            self.botao_opcao_3.configure(state="normal")

        # Chamar função para habilitar os botões quando a janela de configurações for fechada
        aplicativo.app.protocol("WM_DELETE_WINDOW", lambda: [habilitar_botoes(), aplicativo.app.destroy()])

    def opcao_2(self):
        self.botao_opcao_1.configure(state="disabled")
        self.botao_opcao_2.configure(state="disabled")
        self.botao_opcao_3.configure(state="disabled")

        mass_message_app = MassMessageApp(main_app=self.app)
        mass_message_app.run()

        def habilitar_botoes():
            self.botao_opcao_1.configure(state="normal")
            self.botao_opcao_2.configure(state="normal")
            self.botao_opcao_3.configure(state="normal")

        # Chamar função para habilitar os botões quando a janela de configurações for fechada
        mass_message_app.app.protocol("WM_DELETE_WINDOW", lambda: [habilitar_botoes(), mass_message_app.app.destroy()])

    def opcao_3(self):
        self.abrir_menu_configuracoes()

    # Função para abrir o menu de configurações
    def abrir_menu_configuracoes(self):
        self.botao_opcao_1.configure(state="disabled")
        self.botao_opcao_2.configure(state="disabled")
        self.botao_opcao_3.configure(state="disabled")

        config_window = ctk.CTkToplevel(self.app)
        config_window.title("Configurações")
        config_window.geometry("400x350")
        config_window.attributes("-topmost", True)  # Mantém a janela sempre no topo

        # Título do menu de configurações
        titulo_label = ctk.CTkLabel(config_window, text="Menu de Configurações", font=("Cascadia Mono", 25))
        titulo_label.pack(pady=10)

        # Botão para apagar arquivo Excel
        apagar_excel_button = ctk.CTkButton(config_window, text="Apagar Login", command=self.apagar_arquivo_excel,
                                            font=("Cascadia Mono", 13))
        apagar_excel_button.pack(pady=(15, 5))  # Espaçamento menor antes de "Mostrar Login"

        # Botão para mostrar login e senha
        mostrar_login_button = ctk.CTkButton(config_window, text="Mostrar Login", command=self.mostrar_login,
                                             font=("Cascadia Mono", 13))
        mostrar_login_button.pack(pady=(0, 15))  # Deixar "Mostrar Login" bem próximo a "Apagar Login"

        # Caixa de texto para definir número de telefone
        telefone_label = ctk.CTkLabel(config_window, text="Definir Número de Telefone:", font=("Cascadia Mono", 13))
        telefone_label.pack(pady=5)

        # Se já houver um número de telefone salvo, ele será exibido
        telefone_entry = ctk.CTkEntry(config_window, placeholder_text="Insira o número de telefone",
                                      font=("Cascadia Mono", 13))
        telefone_entry.pack(pady=5)

        # Coloca o número salvo na caixa de texto, se existir
        if self.numero_telefone:
            telefone_entry.insert(0, self.numero_telefone)

        aplicar_button = ctk.CTkButton(config_window, text="Aplicar", font=("Cascadia Mono", 13),
                                       command=lambda: self.aplicar_telefone(telefone_entry.get()))
        aplicar_button.pack(pady=15)

        def habilitar_botoes():
            self.botao_opcao_1.configure(state="normal")
            self.botao_opcao_2.configure(state="normal")
            self.botao_opcao_3.configure(state="normal")

        # Chamar função para habilitar os botões quando a janela de configurações for fechada
        config_window.protocol("WM_DELETE_WINDOW", lambda: [habilitar_botoes(), config_window.destroy()])

    # Função para apagar um arquivo Excel
    def apagar_arquivo_excel(self):
        arquivos = ["itens/extras/secret.key", 'itens/extras/login_data.enc']
        arquivos_apagados = []
        erros = []

        for arquivo in arquivos:
            if os.path.exists(arquivo):
                os.remove(arquivo)
                arquivos_apagados.append(arquivo)
            else:
                erros.append(arquivo)

        if arquivos_apagados:
            messagebox.showinfo("Sucesso", f"Arquivos apagados com sucesso")
            self.app.destroy()
            return True
        if erros:
            messagebox.showerror("Erro", f"Login não encontrado")

    # Função para aplicar o número de telefone
    def aplicar_telefone(self, numero):
        if numero and numero.isdigit():  # Verifica se o número foi inserido e é composto apenas de dígitos
            self.numero_telefone = numero
            messagebox.showinfo("Aplicação Concluída", f"O número {numero} foi definido como o telefone principal.")

            # Reescrever o arquivo de credenciais com o novo número de telefone
            try:
                self.login, self.senha, _ = extras.login.load_credentials()  # Carrega as credenciais atuais (login e senha)
                extras.login.save_credentials(self.login, self.senha, numero)  # Salva o login, senha e o novo número
                messagebox.showinfo("Sucesso", "Número de telefone atualizado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao atualizar o número de telefone: {str(e)}")
        else:
            messagebox.showwarning("Aviso", "Por favor, insira um número válido. Apenas números são permitidos.")

    # Função para mostrar login e senha
    def mostrar_login(self):
        messagebox.showinfo("Login", f"Login: {self.login}\nSenha: {self.senha}\nNumero: {self.numero_telefone}")

    # Método para garantir que o fechamento da janela principal seja controlado

    def run(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("themes/violet.json")

        self.app = ctk.CTk()
        self.app.title("Menu Principal")
        self.app.geometry("600x500")

        logo_path = "itens/logo.png"
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((300, 150))
        logo_image_ctk = ctk.CTkImage(light_image=logo_image, size=(300, 150))

        self.logo_label = ctk.CTkLabel(self.app, text="", image=logo_image_ctk)
        self.logo_label.pack(pady=20)

        botao_tamanho_inicial = 300
        botao_altura_inicial = 70

        self.botao_opcao_1 = ctk.CTkButton(self.app, text="Aluno Presente", command=self.opcao_1,
                                           width=botao_tamanho_inicial,
                                           height=botao_altura_inicial, font=("Cascadia Mono", 20))
        self.botao_opcao_1.pack(pady=5)

        self.botao_opcao_2 = ctk.CTkButton(self.app, text="Mensagem em Massa", command=self.opcao_2,
                                           width=botao_tamanho_inicial,
                                           height=botao_altura_inicial, font=("Cascadia Mono", 20))
        self.botao_opcao_2.pack(pady=5)

        self.botao_opcao_3 = ctk.CTkButton(self.app, text="Configurações", command=self.opcao_3,
                                           width=botao_tamanho_inicial, height=botao_altura_inicial,
                                           font=("Cascadia Mono", 20))
        self.botao_opcao_3.pack(pady=5)

        self.app.mainloop()


if __name__ == "__main__":
    print("\n\nMuito obrigado por usar o nosso Programa!, Feito por Vitor, "
          "Leoni e Yuri 2A, orientado pelo professor Vinicius")
    try:
        usuario, senha, numero_telefone = extras.login.login()
    except:
        exit()
    menu_app = MenuApp(usuario,senha,numero_telefone)
    menu_app.run()
