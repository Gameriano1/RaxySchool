import pandas as pd
from itens.contabilizador import FrequenciaEdu
from itens import enviar

class RaxySchool:
    def __init__(self, grauescolaridade, datas, mensagem=False, quantidade=None, numero_telefone=None):
        self.numero = numero_telefone
        self.mensagem = mensagem
        self.quantidade = quantidade
        self.metodo = grauescolaridade
        self.datas = datas
        self.contagens = [["1A", "Yuri Fonseca Ramos", ["20/10/2024", "21/10/2024"]], ["2A", "Vitor Fonseca Ramos", ["22/10/2024", "23/10/2024"]], ["2A", "vinicius Fonseca Ramos", ["20/10/2024", "21/10/2024", "40/30/1999"]], ["9B", "leoni Fonseca Ramos", ["02/10/2024"]]]

    def contabilizar(self):
        print("Contando Alunos e faltas...")
        try:
            frequencia_edu = FrequenciaEdu()
            frequencia_edu.realizar_login()
            self.contagens = frequencia_edu.obter_frequencias(self.metodo, self.datas)  # Populate contagens
            return True
        except:
            return False

    def gerar_planilha_alunos_faltas(self):
        print("\nGerando planilha... aguarde!")

        # Cria uma lista de dicionários com as informações dos alunos que faltaram
        dados_alunos = [
            {'Turma': aluno[0], 'Nome': aluno[1], 'Quantidade Faltas': len(aluno[2]), 'Dias': ", ".join(aluno[2])}
            for aluno in self.contagens
        ]

        # Cria um DataFrame do pandas
        df = pd.DataFrame(dados_alunos)

        # Define o nome do arquivo Excel
        nome_arquivo = f'alunos_atencao.xlsx'

        # Salva o DataFrame em uma planilha Excel
        df.to_excel(nome_arquivo, index=False)

        print(f"Planilha criada: {nome_arquivo}")
        return nome_arquivo

    def run(self):
        try:
            # status = self.contabilizar()
            # if not status:
            #     return False
            planilha = self.gerar_planilha_alunos_faltas()

            if self.mensagem and self.quantidade:
                # Send messages if needed
                file_path = 'alunos_atencao.xlsx'
                df = pd.read_excel(file_path)
                alunos = enviar.alunos_com_faltas(df, int(self.quantidade))

                file_path = 'itens/numeros.xlsx'
                df = pd.read_excel(file_path)

                alunosmensagem = []
                for aluno in alunos:
                    numero = enviar.buscar_numero_por_nome(df, aluno[0], aluno[1], aluno[2])
                    if numero:
                        alunosmensagem.append(numero)

                mensagem = f"""Sr(a) nomeresponsavel
                
A gestão da escola João Firmino comunica que o estudante nomealuno , da turma serie , esteve ausente nos dias

datasfaltas .
"""
                if alunosmensagem:
                    mensagem_final, navegador = enviar.enviar_mensagens_em_lote(alunosmensagem, mensagem)

                    enviar.enviar_mensagem(navegador, self.numero, texto=mensagem_final)
                    enviar.sair_da_conta(navegador)
                    navegador.quit()
                    print("Finalizado!!!")
                else:
                    print("Nenhum número de aluno encontrado!")

            return planilha

        except Exception as e:
            print(f"Um erro ocorreu:\n {e}")
            return False


if __name__ == '__main__':
    escolaridade = "Ensino Fundamental"
    raxy = RaxySchool(escolaridade, ['11/10/2024'])
    lista = raxy.run()

    print("\n\nMuito obrigado por usar o nosso Programa!, Feito por Vitor, "
          "Leoni e Yuri 2A, orientado pelo professor Vinicius")
