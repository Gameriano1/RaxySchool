from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
from datetime import datetime
from .extras import login

import time

class FrequenciaEdu:
    def __init__(self):
        self.usuario, self.senha, self.telefone = login.login()

        if not "rg" in self.usuario:
            self.usuario = "rg" + self.usuario

        if not "sp" in self.usuario:
            self.usuario = self.usuario + "sp"

        self.s = requests.Session()
        self.s.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
            'Referer': 'https://frequencia.sed.educacao.sp.gov.br/Frequencia/Index'
        }
        self.alunos = []  # This will hold student data

    def realizar_login(self):
        payload = f'usuario={self.usuario}&senha={self.senha}'
        self._tentar_request(self.s.post, 'https://sed.educacao.sp.gov.br/Logon/LogOn/', data=payload)
        self._tentar_request(self.s.post, 'https://sed.educacao.sp.gov.br/Inicio/AlterarPerfil', data='id=114')

    def obter_frequencias(self, metodo, datas):
        estado = self._tentar_request(self.s.post,
                                      'https://frequencia.sed.educacao.sp.gov.br/Filtro/FiltroRedesEnsino',
                                      data=f'anoLetivo={datetime.now().year}').json()[0]["Value"]

        diretoria = self._tentar_request(self.s.post,
                                         'https://frequencia.sed.educacao.sp.gov.br/Filtro/FiltroDiretorias',
                                         data=f'idRedeEnsino={estado}').json()[0]["Value"]

        municipio = self._tentar_request(self.s.post,
                                         'https://frequencia.sed.educacao.sp.gov.br/Filtro/FiltroMunicipios',
                                         data=f'idDiretoria={diretoria}&idRedeEnsino={estado}').json()[0]["Value"]

        escola = self._tentar_request(self.s.post,
                                      'https://frequencia.sed.educacao.sp.gov.br/Filtro/FiltroEscolas',
                                      data=f'idRedeEnsino={estado}&idDiretoria={diretoria}&idMunicipio={municipio}&stFuncionamentoEscola=1&anoLetivo={datetime.now().year}').json()[0]["Value"]

        tipoensino = self._tentar_request(self.s.post,
                                          'https://frequencia.sed.educacao.sp.gov.br/Filtro/FiltroTiposEnsino',
                                          data=f'nrAnoLetivo={datetime.now().year}&idRedeEnsino={estado}&idDiretoria={diretoria}&idEscola={escola}').json()

        print("Pesquisando alunos nas salas...\n")
        for i in tipoensino:
            texto = i["Text"].lower()
            for substring in ["novo", "9 anos", "itinerário"]:
                if substring in texto:
                    salas = self._tentar_request(self.s.post,
                                                 'https://frequencia.sed.educacao.sp.gov.br/Filtro/FiltroTurma',
                                                 data=f'CodigoEscola={escola}&CodigoTipoEnsino={i["Value"]}&AnoLetivo={datetime.now().year}&CodigoDiretoria={diretoria}').json()

                    for x in salas:
                        materias = self._pesquisar_materias(x["Value"], tipoensino)
                        hora = '13:45 às 14:30' if metodo == "Ensino Fundamental" else '07:45 às 08:30'
                        for data in datas:
                            self.listar_alunos_faltaram(materias[0]["Value"], x["Value"], escola, hora, data)

        print("Coletando alunos para exportação...\n")
        return self.alunos  # Return the collected student data

    def _pesquisar_materias(self, turma_value, tipoensino):
        retorno = self._tentar_request(self.s.post,
                                       'https://frequencia.sed.educacao.sp.gov.br/Filtro/FiltroDisciplina',
                                       data=f'TipoEnsino={tipoensino}&CodigoTurma={turma_value}&AnoLetivo={datetime.now().year}').json()
        return retorno

    def listar_alunos_faltaram(self, disciplina, turma, escola, horario, data):
        substituicoes = {
            "A1": "2A", "A3": "3A",
            "B2": "2B", "B3": "3B",
            "C2": "2C", "C4": "3C",
            "D2": "2D", "D4": "3D"
        }

        payload = {
            'data': data,
            'disciplina': disciplina,
            'turma': turma,
            'subturma': "0",
            'escola': escola,
            'horario': horario,
            'redeEnsino': '1',
            'nrRA': '',
            'nrDigRa': '',
            'sgUfRa': ''
        }

        payload_encoded = urlencode(payload)
        solicitacao = self._tentar_request(self.s.post, 'https://frequencia.sed.educacao.sp.gov.br/Frequencia/FrequenciaParcial', data=payload_encoded)

        if solicitacao.status_code != 200:
            print(f"Erro ao enviar solicitação: {solicitacao.status_code}")
            return False

        soup = BeautifulSoup(solicitacao.text, "html.parser")

        try:
            serie = soup.select_one("#tabs ul.nav li.active a").text.strip()
        except:
            return False

        if "NÃO" in serie:
            serie = substituicoes[serie.split(" ")[3]]
        else:
            serie = serie.split(" ")[0][0] + serie.split(" ")[2]

        alunos_faltaram = self._processar_tabela_faltas(soup, serie)

        for aluno in alunos_faltaram:
            aluno_ja_registrado = False
            for registro in self.alunos:
                if registro[1] == aluno[0] and registro[0] == serie:
                    aluno_ja_registrado = True
                    registro[2].append(data)
                    break

            if not aluno_ja_registrado:
                self.alunos.append([serie, aluno[0], [data]])
        return True

    def _processar_tabela_faltas(self, soup, serie):
        linhas = soup.select("table#frequencias tbody tr")
        alunos_faltaram = []

        for linha in linhas:
            situacao = linha.find("td", string="Ativo")
            if situacao:
                aluno_td = linha.select_one("td:nth-of-type(3)")
                numero_td = linha.select_one("td:nth-of-type(1)")
                if aluno_td and numero_td:
                    aluno = aluno_td.text.strip()
                    circulo_falta = linha.find("div", class_="circuloVermelho")
                    if circulo_falta:
                        alunos_faltaram.append([aluno, serie])

        return alunos_faltaram

    def _tentar_request(self, func, url, **kwargs):
        tentativas = 5
        for tentativa in range(tentativas):
            try:
                response = func(url, **kwargs)
                if response.status_code == 200:
                    return response
            except requests.RequestException as e:
                print(f"Erro na tentativa {tentativa + 1} de {tentativas}: {e}")
            time.sleep(2)  # Intervalo entre tentativas
        raise Exception(f"Falha após {tentativas} tentativas em {url}")

