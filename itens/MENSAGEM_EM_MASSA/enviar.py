from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import urllib.parse
import re


def buscar_numero_por_nome(df, nome_procurado, datas, serie):
    # Filtrar o DataFrame pelo nome
    aluno_encontrado = df['Unnamed: 2'].str.contains(nome_procurado, case=False, na=False)

    if aluno_encontrado.any():  # Se houver pelo menos um True na série booleana
        numero = str(df.loc[aluno_encontrado, 'Unnamed: 5'].values[0]).strip()  # Acessar o número correspondente
        numero = ''.join(re.findall(r'\d+', numero))

        if len(str(numero)) < 13:
            numero = '55' + str(numero)

        print(numero) if numero != "55" else None

        pai = df.loc[aluno_encontrado, 'Unnamed: 3'].values[0]
        return [numero, pai, nome_procurado, datas, serie]
    else:
        return None


def alunos_com_faltas(df, numerofaltas):
    # Converter a coluna de faltas para inteiro, se necessário
    df['Quantidade Faltas'] = pd.to_numeric(df['Quantidade Faltas'], errors='coerce')

    # Filtrar os alunos com faltas maior ou igual a X
    alunos_faltosos = df[df['Quantidade Faltas'] >= numerofaltas]

    # Iterar sobre os alunos filtrados e printar nome e quantidade de faltas
    alunos = []
    for index, row in alunos_faltosos.iterrows():
        alunos.append([row['Nome'], row['Dias'].replace(', ', '\n'), row['Turma']])
    return alunos


def configurar_navegador():
    navegador = webdriver.Chrome()
    navegador.get("http://web.whatsapp.com/")
  
    while len(navegador.find_elements(By.ID, 'side')) < 1:
        continue
    
    return navegador


def preparar_mensagem(mensagem, nome, pais, datas, serie):
    mensagem_personalizada = mensagem.replace("nomeresponsavel", pais)
    mensagem_personalizada = mensagem_personalizada.replace("nomealuno", nome)
    mensagem_personalizada = mensagem_personalizada.replace("datasfaltas", datas)
    mensagem_personalizada = mensagem_personalizada.replace("serie", serie)
    return mensagem_personalizada


def enviar_mensagem(navegador, telefone, texto):
    link = f"https://web.whatsapp.com/send?phone={telefone}&text={urllib.parse.quote(texto)}"
    navegador.get(link)
    
    while len(navegador.find_elements(By.ID, 'side')) < 1:
        continue

    while len(navegador.find_elements(By.XPATH, "//h1[contains(text(), 'Baixar o WhatsApp para Windows')]")) > 0:
        if navegador.find_elements('xpath',
                                   "//*[contains(text(), 'O número de telefone compartilhado por url é inválido.')]"):
            break
        continue
    time.sleep(3)

    if len(navegador.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) > 0:
        raise Exception(f"Erro ao enviar mensagem para o número: {telefone}")
    else:
        navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[2]/button/span').click()
        time.sleep(7)


def sair_da_conta(navegador):
    navegador.find_element('xpath', "//*[@aria-label='Configurações']").click()
    while len(navegador.find_elements(By.XPATH, "//*[contains(text(), 'Desconectar')]")) < 1:
        continue
    navegador.find_element(By.XPATH, "//*[contains(text(), 'Desconectar')]").click()
    navegador.find_element(By.XPATH, "//*[contains(text(), 'Desconectar')]").click()
    while len(navegador.find_elements(By.XPATH, "//*[contains(text(), 'Use o Whatsapp no seu computador')]")) > 1:
        continue
    while len(navegador.find_elements(By.XPATH, "//h1[contains(text(), 'Baixar o WhatsApp para Windows')]")) < 0:
        continue
    time.sleep(5)


def criar_arquivo_excel(dados, filename):
    df = pd.DataFrame(dados, columns=["Aluno", "Pai(s)", "Número", "Turma"])
    df.to_excel(filename, index=False)


def enviar_mensagens_em_lote(numeros, mensagem):
    navegador = configurar_navegador()

    numeros_invalidos = []
    alunos_validos = []

    for numero in numeros:
        nomealuno = numero[2]
        pai = numero[1]
        datas = numero[3]
        serie = numero[4]


        if numero[0] == "55":
            numero[0] = ''
            numeros_invalidos.append([nomealuno, "Inválido", "Inválido", serie])
            continue


        texto = preparar_mensagem(mensagem, nomealuno, pai, datas, serie)
        print(f"Enviando mensagem para: {nomealuno}, {pai}, {datas}")

        try:
            enviar_mensagem(navegador, numero[0], texto)
            alunos_validos.append([nomealuno, pai, numero[0], serie])  # Adiciona os alunos válidos à lista
        except Exception as e:
            print(e)
            numeros_invalidos.append([nomealuno, pai, numero[0], serie])  # Adiciona número inválido à lista

    if numeros_invalidos:
        mensagem_final = "Números inválidos e nome dos pais:" + "".join(
            [f"\n\n   Aluno: {n[0]} do {n[3]}, nome do pai(s): {n[1]} e o número: {n[2]}" for n in numeros_invalidos]
        )
    else:
        mensagem_final = "Nenhum número inválido encontrado."
    
    criar_arquivo_excel(numeros_invalidos, "Numeros_invalidos.xlsx")
    criar_arquivo_excel(alunos_validos, "Alunos_validos.xlsx")

    return mensagem_final, navegador


if __name__ == "__main__":
    file_path = '../alunos_atencao.xlsx'

    df = pd.read_excel(file_path)

    numerofaltas = 2
    alunos = alunos_com_faltas(df, numerofaltas)

    file_path = 'numeros.xlsx'
    df = pd.read_excel(file_path)

    alunosmensagem = []
    for aluno in alunos:

        numero = buscar_numero_por_nome(df, aluno[0], aluno[1], aluno[2])
        if numero:
            alunosmensagem.append(numero)

    mensagem = """Sr(a) nomeresponsavel
    A gestão da escola João Firmino comunica que o estudante nomealuno, da turma serie, esteve ausente nos dias:
datasfaltas .
    """

    mensagem_final, navegador = enviar_mensagens_em_lote(alunosmensagem, mensagem)

    enviar_mensagem(navegador, '5511983079381', texto=mensagem_final)
    sair_da_conta(navegador)
    navegador.quit()
