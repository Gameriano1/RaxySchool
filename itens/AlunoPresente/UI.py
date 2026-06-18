#  Copyright (c) 2024. Este site e todo o seu conteúdo, incluindo, mas não se limitando a textos, gráficos, logotipos, ícones, imagens, vídeos, áudios, software e qualquer outro material digital, são de propriedade exclusiva da Raxy ou de seus licenciadores. A reprodução, distribuição, modificação, exibição pública ou privada, transmissão ou qualquer outro uso não autorizado do conteúdo deste site é estritamente proibido sem o consentimento prévio por escrito da Raxy.
#
#  O nome "Raxy" e todas as marcas comerciais, logotipos e marcas de serviço exibidos neste aplicativo são propriedade da Raxy. Qualquer uso não autorizado dessas marcas comerciais é proibido.
#
#  A Raxy reserva-se o direito de modificar ou atualizar este aviso de copyright a qualquer momento, sem aviso prévio. O uso contínuo do site após tais alterações constitui sua aceitação das novas condições.

import os
import threading
from datetime import datetime, timedelta
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image, ImageSequence
from tkcalendar import Calendar

from .main import RaxySchool



class JFapp:

    def __init__(self, numero=None, app=None):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("themes/violet.json")
        self.numero_telefone = numero
        self.main_app = app  # A janela principal será passada aqui
        self.app = None  # A nova janela será inicializada aqui
        self.dias = None
        self.mensagem = None
        self.loading_label = None
        self.gif_frames = None
        self.loading_gif_active = False
        self.gif_iterator = None



    def is_dia_util(self, data):
        dia_semana = data.weekday()
        return dia_semana < 5

    def listar_datas_uteis_no_intervalo(self, data_inicio, data_fim):
        start_date = datetime.strptime(data_inicio, "%d/%m/%Y")
        end_date = datetime.strptime(data_fim, "%d/%m/%Y")

        delta = timedelta(days=1)
        datas_uteis = []

        while start_date <= end_date:
            if self.is_dia_util(start_date):
                datas_uteis.append(start_date.strftime("%d/%m/%Y"))
            start_date += delta
        return datas_uteis

    def selecionar_intervalo(self):
        try:
            data_inicio = self.calendario_inicio.get_date()
            data_fim = self.calendario_fim.get_date()

            if data_inicio > data_fim:
                messagebox.showerror("Erro", "A data de início não pode ser maior que a data de fim.")
                return
            else:
                return self.listar_datas_uteis_no_intervalo(data_inicio, data_fim)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao selecionar intervalo: {e}")

    def run_task(self, nivel_ensino, datas, numero_telefone):
        raxy = RaxySchool(nivel_ensino, datas, self.mensagem, self.dias, numero_telefone)
        response = raxy.run()
        if not response:
            self.loading_gif_active = False
            self.update_status("Erro")
            self.button.configure(state="normal")
        else:
            try:
                os.startfile('alunos_atencao.xlsx')
            except:
                pass
            self.loading_gif_active = False
            self.update_status("Concluído!")
            self.button.configure(state="normal")

    def animate_gif(self):
        if self.loading_gif_active and self.gif_frames:
            try:
                frame = next(self.gif_iterator)
            except StopIteration:
                self.gif_iterator = iter(self.gif_frames)
                frame = next(self.gif_iterator)

            if self.loading_label and self.loading_label.winfo_exists():
                self.loading_label.configure(image=frame)
                self.loading_label.image = frame
                # Checar se a função after ainda pode ser chamada no widget
                if self.loading_label.winfo_exists():
                    self.loading_label.after(100, self.animate_gif)

    def update_status(self, status_text):
        # Verifica se o widget ainda existe antes de manipular
        if self.loading_label and self.loading_label.winfo_exists():
            self.loading_label.destroy()  # Destrói o widget existente

        # Cria um novo widget com base no status recebido
        if "Concluído" in status_text:
            self.loading_label = ctk.CTkLabel(self.app, text="", font=("Cascadia Mono", 15))
        elif "Encerrar" in status_text:
            self.loading_label = ctk.CTkLabel(self.app, text="")
        elif "Erro" in status_text:
            self.loading_label = ctk.CTkLabel(self.app, text="Erro!", font=("Cascadia Mono", 15))
        else:
            self.loading_label = ctk.CTkLabel(self.app, text='', font=("Cascadia Mono", 15))

        # Verifique se o app ainda está ativo antes de adicionar o widget ao layout
        if self.app and self.app.winfo_exists():
            self.loading_label.grid(row=6, column=0, pady=10, sticky="n")

    def on_button_click(self):
        nivel_ensino = self.option_menu.get()
        if nivel_ensino.__contains__('Escolha'):
            messagebox.showerror("Erro", "Escolha um nível de ensino válido")
            return

        datas = self.selecionar_intervalo()
        if not datas:
            return

        self.button.configure(state="disabled")

        if self.loading_label and self.loading_label.winfo_exists() and "Concluído" in self.loading_label.cget("text"):
            self.loading_label.destroy()
            self.loading_label = ctk.CTkLabel(self.app, text="")
            self.loading_label.grid(row=6, column=0, pady=10, sticky="n")

        self.loading_gif_active = True
        self.update_status("Carregando...")

        self.animate_gif()

        threading.Thread(target=self.run_task, args=(nivel_ensino, datas, self.numero_telefone)).start()

    def abrir_opcoes_avancadas(self):
        self.app.attributes("-topmost", False)

        opcoes_window = ctk.CTkToplevel(self.app)
        opcoes_window.title("Opções Avançadas")
        opcoes_window.iconbitmap('itens/AlunoPresente/JF.ico')
        opcoes_window.geometry("400x300")

        opcoes_window.attributes("-topmost", True)
        opcoes_window.grab_set()

        label_quantidade_falta = ctk.CTkLabel(opcoes_window, text="Quantidade de Faltas:", font=("Cascadia Mono", 15))
        label_quantidade_falta.pack(pady=25)
        input_quantidade_falta = ctk.CTkEntry(opcoes_window)
        input_quantidade_falta.pack(pady=0)

        # Definir o valor da entrada se disponível
        if self.dias:
            input_quantidade_falta.insert(0, self.dias)

        checkbox_enviar_mensagem = ctk.CTkCheckBox(opcoes_window, text="Enviar Mensagem", font=("Cascadia Mono", 15))
        checkbox_enviar_mensagem.pack(pady=30)

        # Definir o estado do checkbox
        checkbox_enviar_mensagem.select() if self.mensagem else checkbox_enviar_mensagem.deselect()


        button_aplicar = ctk.CTkButton(opcoes_window, text="Aplicar",
                                       command=lambda: self.aplicar_opcoes_avancadas(input_quantidade_falta.get(),
                                                                                     checkbox_enviar_mensagem.get()),
                                       font=("Cascadia Mono", 15))
        button_aplicar.pack(pady=10)

        self.status_label = ctk.CTkLabel(opcoes_window, text="", font=("Cascadia Mono", 15))
        self.status_label.pack(pady=10)

        def fechar_opcoes():
            opcoes_window.grab_release()  # Libera a janela modal
            opcoes_window.destroy()  # Fecha a janela de opções
            self.app.attributes("-topmost", True)

        opcoes_window.protocol("WM_DELETE_WINDOW", fechar_opcoes)

    def aplicar_opcoes_avancadas(self, quantidade_falta, enviar_mensagem):
        if not quantidade_falta.isdigit():
            messagebox.showerror("Erro", "Escolha um número válido")
            return
        self.mensagem = enviar_mensagem
        self.dias = quantidade_falta
        self.status_label.configure(text="Aplicado!")  # Atualiza o texto do rótulo na janela de opções

    def main(self):
        # Criar uma nova janela Toplevel em vez de usar a janela principal
        self.app = ctk.CTkToplevel(self.main_app)  # Cria uma nova janela Toplevel
        self.app.iconbitmap('itens/AlunoPresente/JF.ico')
        self.app.title("Raxy School APP")
        self.app.geometry("750x750")
        self.app.resizable(True, True)
        self.app.attributes("-topmost", True)

        # Layout responsivo para a janela
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        # Imagem do logo redimensionável
        image_path = "itens/logo.png"
        logo_image = Image.open(image_path)
        logo_image = logo_image.resize((300, 150))  # Redimensiona a imagem logo
        logo_image_ctk = ctk.CTkImage(light_image=logo_image, size=(300, 150))

        label_logo = ctk.CTkLabel(self.app, image=logo_image_ctk, text="")
        label_logo.grid(row=0, column=0, pady=25, sticky="n")

        # Menu suspenso com opções
        nivel_ensino_options = ["Ensino Fundamental", "Ensino Médio"]
        option_menu = ctk.CTkOptionMenu(self.app, values=nivel_ensino_options, font=("Cascadia Mono", 15), width=300)
        self.option_menu = option_menu
        option_menu.set("Escolha o nível de ensino")
        option_menu.grid(row=1, column=0, pady=25, sticky="n")

        # Frame para os calendários
        frame_calendarios = ctk.CTkFrame(self.app, border_width=0, fg_color="transparent")
        frame_calendarios.grid(row=2, column=0, pady=10, sticky="nsew")

        frame_calendarios.grid_rowconfigure(0, weight=1)
        frame_calendarios.grid_columnconfigure((0, 1), weight=1)

        calendario_inicio = Calendar(frame_calendarios, selectmode="day", date_pattern="dd/mm/yyyy",
                                     selectbackground='purple', font=("Cascadia Mono", 10), background='purple4')
        self.calendario_inicio = calendario_inicio
        calendario_inicio.grid(row=0, column=0, padx=10, sticky="e")

        calendario_fim = Calendar(frame_calendarios, selectmode="day", date_pattern="dd/mm/yyyy",
                                  selectbackground='purple', font=("Cascadia Mono", 10), background='purple4')
        self.calendario_fim = calendario_fim
        calendario_fim.grid(row=0, column=1, padx=10, sticky="w")

        button_opcoes_avancadas = ctk.CTkButton(self.app, text="Opções Avançadas", command=self.abrir_opcoes_avancadas,
                                                fg_color='medium purple', font=("Cascadia Mono", 12))
        button_opcoes_avancadas.grid(row=3, column=0, pady=20, sticky="n")

        self.button = ctk.CTkButton(self.app, text="Enviar", command=self.on_button_click, width=400, height=70,
                                    font=("Cascadia Mono", 30))
        self.button.grid(row=4, column=0, pady=20, sticky="n")

        self.loading_label = ctk.CTkLabel(self.app, text="")
        self.loading_label.grid(row=5, column=0, pady=10, sticky="n")

        # Carregar gif
        gif_path = "itens/loading.gif"
        gif_image = Image.open(gif_path)

        gif_width, gif_height = 50, 50
        self.gif_frames = [ctk.CTkImage(light_image=frame.convert("RGBA").resize((gif_width, gif_height)),
                                        size=(gif_width, gif_height))
                           for frame in ImageSequence.Iterator(gif_image)]

        self.gif_iterator = iter(self.gif_frames)

if __name__ == '__main__':
    print("\n\nMuito obrigado por usar o nosso Programa!, Feito por Vitor, "
          "Leoni e Yuri 2A, orientado pelo professor Vinicius")
    app = JFapp()
    app.main()
