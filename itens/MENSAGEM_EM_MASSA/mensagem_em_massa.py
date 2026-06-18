import math
import os
import re
import time
import urllib
import pandas as pd
from tkinter import filedialog, messagebox
from PIL import Image, ImageSequence
from selenium import webdriver
from selenium.webdriver.common.by import By
import customtkinter as ctk
import threading
import urllib.parse
import logging

# Desativa logs da biblioteca customtkinter, se ela estiver usando logging
logging.getLogger('customtkinter').setLevel(logging.CRITICAL)


class MassMessageApp:
    def __init__(self, main_app=None):
        self.main_app = main_app  # Janela principal
        self.app = None  # Para a nova janela
        self.caminho_arquivo = None
        self.mensagem_entry = None
        self.botao_enviar = None
        self.loading_label = None
        self.loading_gif_active = False
        self.gif_frames = None
        self.gif_iterator = None

    def enviar_mensagem(self, navegador, telefone, texto):
        link = f"https://web.whatsapp.com/send?phone={telefone}&text={urllib.parse.quote(texto)}"
        navegador.get(link)

        while len(navegador.find_elements(By.ID, 'side')) < 1:
            continue

        while len(navegador.find_elements(By.XPATH, "//h1[contains(text(), 'Baixar o WhatsApp para Windows')]")) > 0:
            if navegador.find_elements(By.XPATH,
                                       "//*[contains(text(), 'O número de telefone compartilhado por url é inválido.')]"):
                break
            continue
        time.sleep(3)

        if len(navegador.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) > 0:
            raise Exception(f"Erro ao enviar mensagem para o número: {telefone}")
        else:
            navegador.find_element(By.XPATH,
                                   '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[2]/button/span').click()
            time.sleep(7)

    def enviar_mensagens_arquivo(self, arquivo_excel, texto_mensagem):
        df = pd.read_excel(arquivo_excel)
        navegador = None

        try:
            navegador = webdriver.Chrome()
            navegador.get("https://web.whatsapp.com")

            while len(navegador.find_elements(By.ID, 'side')) < 1:
                continue

            numeros_invalidos = []

            for index, row in df.iterrows():
                telefone = row['Unnamed: 5']
                aluno_nome = row['Unnamed: 2']
                pai_nome = row['Unnamed: 3']

                if pd.isna(telefone) or not isinstance(telefone, str):
                    telefone = str(telefone) if not math.isnan(telefone) else ''

                telefone = ''.join(re.findall(r'\d+', telefone))

                if len(str(telefone)) < 13:
                    telefone = '55' + str(telefone)

                if telefone:
                    try:
                        if telefone != "55":
                            print(f"Mensagem enviada para {telefone}")
                            self.enviar_mensagem(navegador, telefone, texto_mensagem)
                            time.sleep(7)
                    except Exception as e:
                        print(f"Falha ao enviar para {telefone}: {e}")
                        numeros_invalidos.append((aluno_nome, pai_nome, telefone))

            if numeros_invalidos:
                invalid_numbers_text = "Os seguintes números são inválidos:\n" + "\n".join(
                    [f"Aluno: {aluno}, Pai: {pai}, Telefone: {tel}" for aluno, pai, tel in numeros_invalidos])
                messagebox.showinfo("Números Inválidos", invalid_numbers_text)

        except Exception as e:
            print(f"Erro durante a execução: {e}")
            if navegador:
                navegador.quit()
            self.loading_gif_active = False
            self.update_status("Encerrar")
            self.botao_enviar.configure(state="normal")

    def escolher_arquivo(self):
        self.app.attributes("-topmost", False)
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
        if arquivo:
            self.caminho_arquivo.set(arquivo)
        self.app.attributes("-topmost", True)

    def iniciar_envio(self):
        arquivo_excel = self.caminho_arquivo.get()
        texto_mensagem = self.mensagem_entry.get("1.0", "end").strip()

        if not os.path.isfile(arquivo_excel):
            messagebox.showwarning("Caminho Inválido", "Por favor, forneça um caminho válido para o arquivo Excel.")
            return

        if not arquivo_excel or not texto_mensagem:
            messagebox.showwarning("Campos obrigatórios", "Por favor, selecione o arquivo e digite a mensagem.")
            return

        self.botao_enviar.configure(state="disabled")

        if self.loading_label.winfo_exists() and "Concluído" in self.loading_label.cget("text"):
            self.loading_label.destroy()
            self.loading_label = ctk.CTkLabel(self.app, text="")
            self.loading_label.pack(pady=10)  # Usando pack() no lugar de grid()

        self.loading_gif_active = True
        self.update_status("Carregando...")

        self.animate_gif()

        threading.Thread(target=self.enviar_mensagens_arquivo,
                         args=(arquivo_excel, texto_mensagem)).start()

    def update_status(self, status_text):
        if "Concluído" in status_text:
            if self.loading_label.winfo_exists():
                self.loading_label.destroy()

            self.loading_label = ctk.CTkLabel(self.app, text="Concluído", font=("Cascadia Mono", 15))
            self.loading_label.pack(pady=10)  # Usando pack() no lugar de grid()
        elif "Encerrar" in status_text:
            if self.loading_label.winfo_exists():
                self.loading_label.destroy()
            self.loading_label = ctk.CTkLabel(self.app, text="")
            self.loading_label.pack(pady=10)

    def animate_gif(self):
        if self.loading_gif_active and self.gif_frames:
            try:
                frame = next(self.gif_iterator)
            except StopIteration:
                self.gif_iterator = iter(self.gif_frames)
                frame = next(self.gif_iterator)

            self.loading_label.configure(image=frame)
            self.loading_label.image = frame
            self.loading_label.after(100, self.animate_gif)

    def run(self):
        self.app = ctk.CTkToplevel(self.main_app)  # Modificação para criar uma nova janela no contexto do app principal
        self.app.title("Envio de Mensagens em Massa")
        self.app.geometry("750x800")

        logo_path = "itens/logo.png"
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((400, 200))

        logo_image_ctk = ctk.CTkImage(light_image=logo_image, size=(400, 200))

        logo_label = ctk.CTkLabel(self.app, text="", image=logo_image_ctk)
        logo_label.pack(pady=10)

        label_arquivo = ctk.CTkLabel(self.app, text="Selecione o arquivo Excel:", font=("Cascadia Mono", 20))
        label_arquivo.pack(pady=20)

        self.caminho_arquivo = ctk.StringVar()
        arquivo_entry = ctk.CTkEntry(self.app, textvariable=self.caminho_arquivo, width=350, font=("Cascadia Mono", 16))
        arquivo_entry.pack(pady=10)

        botao_arquivo = ctk.CTkButton(self.app, text="Escolher Arquivo", command=self.escolher_arquivo, width=350,
                                      font=("Cascadia Mono", 18))
        botao_arquivo.pack(pady=20)

        label_mensagem = ctk.CTkLabel(self.app, text="Digite a mensagem a ser enviada:", font=("Cascadia Mono", 20))
        label_mensagem.pack(pady=20)

        self.mensagem_entry = ctk.CTkTextbox(self.app, height=120, width=400, font=("Cascadia Mono", 16))
        self.mensagem_entry.pack(pady=10)

        self.botao_enviar = ctk.CTkButton(self.app, text="Enviar Mensagens", command=self.iniciar_envio, width=400,
                                          height=70,
                                          font=("Cascadia Mono", 26))
        self.botao_enviar.pack(pady=20)

        gif_path = "itens/loading.gif"
        gif_image = Image.open(gif_path)

        gif_width, gif_height = 50, 50
        self.gif_frames = [ctk.CTkImage(light_image=frame.convert("RGBA").resize((gif_width, gif_height)),
                                        size=(gif_width, gif_height))
                           for frame in ImageSequence.Iterator(gif_image)]
        self.gif_iterator = iter(self.gif_frames)

        self.loading_label = ctk.CTkLabel(self.app, text="")
        self.loading_label.pack(pady=10)  # Usando pack() no lugar de grid()

        # Tornar a janela modal (opcional)
        self.app.grab_set()

        # Garantir que a janela seja sempre visível no topo (opcional)
        self.app.attributes("-topmost", True)

        # Definir comportamento ao fechar a janela (opcional)
        def fechar_janela():
            self.app.grab_release()  # Libera o controle da janela modal
            self.app.destroy()  # Fecha a janela

        self.app.protocol("WM_DELETE_WINDOW", fechar_janela)


# Executa o aplicativo
if __name__ == "__main__":
    app = MassMessageApp()
    app.run()
