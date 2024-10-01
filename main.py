import glob
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import pandas as pd




class RaxySchool:

    def __init__(self):
        caminho_json = 'alunos_fundamental.json'
        self.caminho_json = caminho_json


        if os.path.exists(caminho_json):
            with open(caminho_json, 'r', encoding='utf-8') as json_file:
                self.dados_json = json.load(json_file)
        else:
            self.dados_json = {}

        self.htms = glob.glob('*.htm')

        self.data_atual = datetime.now().strftime("%d-%m-%Y")

    def manter_tres_ultimos_dias(self, quantidade):
        with open(self.caminho_json, 'r', encoding='utf-8') as f:
            self.dados_json = json.load(f)
        for serie in self.dados_json:
            dates = [datetime.strptime(date, "%d-%m-%Y") for date in self.dados_json[serie].keys()]

            dates.sort()

            if len(dates) > quantidade:
                latest_dates = dates[-quantidade:]
                new_series_data = {date.strftime("%d-%m-%Y"): self.dados_json[serie][date.strftime("%d-%m-%Y")] for date in
                                   latest_dates}
                self.dados_json[serie] = new_series_data
        with open(self.caminho_json, 'w', encoding='utf-8') as json_file:
            json.dump(self.dados_json, json_file, ensure_ascii=False, indent=4)

    def analiseHtm(self, variavel):
        for htm in self.htms:
            with open(htm, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')

            table = soup.find('table')
            alunos_fundamental = []
            for row in table.find_all('tr')[1:]:
                columns = row.find_all('td')
                if len(columns) > 1:
                    nome_aluno = columns[1].text.strip()
                    nome_turma = columns[3].text.strip()

                    if any(variavel in column.text for column in columns):
                        alunos_fundamental.append((nome_aluno, nome_turma))

            for aluno, turma in alunos_fundamental:

                if turma not in self.dados_json:
                    self.dados_json[turma] = {}

                if self.data_atual not in self.dados_json[turma]:
                    self.dados_json[turma][self.data_atual] = []

                if aluno not in self.dados_json[turma][self.data_atual]:
                    self.dados_json[turma][self.data_atual].append(aluno)

                with open(self.caminho_json, 'w', encoding='utf-8') as json_file:
                    json.dump(self.dados_json, json_file, ensure_ascii=False, indent=4)

    def contagem_alunos(self, quantidade):
        if os.path.isfile(self.caminho_json):

            with open(self.caminho_json, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            contagem_alunos = {}

            for turma, datas in dados.items():
                for data, alunos in datas.items():
                    for aluno in alunos:
                        if aluno not in contagem_alunos:
                            contagem_alunos[aluno] = set()
                        contagem_alunos[aluno].add(data)

            alunos = []
            for aluno, dias in contagem_alunos.items():
                if len(dias) >= quantidade:
                    alunos.append([aluno, dias])
            if len(alunos):
                print(f"Alunos que faltaram mais de {quantidade} dias:")
                for aluno, dias in alunos:
                    print(f'{aluno} Faltou {len(dias)} dias!')

    def montar_planilha(self, quantidade):
        contagem_faltas = {}

        # Contar as faltas por aluno e turma
        for turma, faltas in self.dados_json.items():
            for data, alunos in faltas.items():
                for aluno in alunos:
                    # Chave única: (aluno, turma)
                    chave = (aluno, turma)
                    if chave not in contagem_faltas:
                        contagem_faltas[chave] = 0
                    contagem_faltas[chave] += 1

        # Filtrar alunos que faltaram mais de 3 dias
        alunos_faltaram_mais_de_tres_dias = {chave: faltas for chave, faltas in contagem_faltas.items() if faltas >= quantidade}

        # Montar a lista de dados filtrados
        dados_faltas_filtrados = []
        for (aluno, turma), total_faltas in alunos_faltaram_mais_de_tres_dias.items():
            dados_faltas_filtrados.append({
                'Turma': turma,
                'Aluno': aluno,
                'Total_Faltas': total_faltas
            })

        # Criar DataFrame e salvar em Excel
        df_faltas = pd.DataFrame(dados_faltas_filtrados)

        arquivo_excel = 'faltas_alunos.xlsx'
        if os.path.isfile(arquivo_excel):
            os.remove(arquivo_excel)
        df_faltas.to_excel(arquivo_excel, index=False)

        print(f"\nOs dados foram salvos em {arquivo_excel}")

    def run(self, variavel, quantidade):
        try:
            self.analiseHtm(variavel)
            self.contagem_alunos(quantidade)

            self.manter_tres_ultimos_dias(quantidade)

            self.montar_planilha(quantidade)

        except Exception as e:
            raise Exception(e)
            # print(f"Um erro ocorreu:\n {e}")
        finally:
            print("\n\nMuito obrigado por usar o nosso Programa!, Feito por Vitor, Leoni e Yuri 2A")


if __name__ == '__main__':

    quantiade_faltas = 2

    raxy = RaxySchool()
    raxy.run("NOVO", quantiade_faltas)
