from openai import OpenAI
from dotenv import load_dotenv
import os

class ExecutadorAnalise:

    def __init__(self):
        self.obj = self.inicializa_gpt()


    def inicializa_gpt(self):
        load_dotenv()
        self.cliente = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.modelo = "gpt-4"


    def carrega(self,nome_do_arquivo):
        try:
            with open(nome_do_arquivo,"r") as arquivo:
                dados = arquivo.read()
                return dados
        except IOError as e:
            print(f"Error {e}")

    def salva_arquivo(self,nome_do_arquivo,conteudo):
        try:
            with open(nome_do_arquivo,"w",encoding="utf-8") as arquivo:
                arquivo.write(conteudo)
        except IOError as e:
            print(f'Erro ao salvar o arquivo: {e}')