import openai
import json
from base_execucao_analise import ExecutadorAnalise

class AnaliseTransacoes(ExecutadorAnalise):
    def __init__(self):
        super().__init__()

    def analisa_transacao(self,lista_transacoes):
        print(f"1.Executando analise de Transação")
        prompt_sistema = """
        Analise as transações financeiras a seguir e identifique se cada uma delas
        é uma "Possível Fraude ou deve ser "Aprovada",
        Adicione um atrbuto "Status" com um dos valores: "Possivel Fraude" ou "Aprovado".
        
        Cada nova transação deve ser inserida dentro da lista do JSON
        
        #Possíveis indicações de fraude
        -Transações com valores muito discrepantes
        -transações que ocorrem em locais muito distantes um do outro
        
        Adote o fromato de resposta abaixo para compor sua resposta.
        
        #Formato Saída
        {
        "transacoes:[
            {
            "id":"id",
            "tipo":"crédito ou débito",
            "estabelecimento":"nome do estabelecimento",
            "horário":"horário da transação",
            "valor":"R$ XX,XX",
            "nome_produto":"nome do produto",
            "localização":"cidade - estado (País)"
            "status":""
            }
        ]
        }
        
        """

        prompt_usuario = f"""
        Considere o CSV abaixo, onde cada linha é uma transação diferente: {lista_transacoes}. Sua resposta deve adotar o #Formato de Resposta (apenas um json sem outros comentários)
        """
        lista_mensagens = [
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": prompt_usuario
            }
        ]
        try:
            resposta = self.cliente.chat.completions.create(
                messages=lista_mensagens,
                model= self.modelo
            )
            conteudo = resposta.choices[0].message.content.replace("'",'"')
            json_resultado = json.loads(conteudo) #converte dado para tipo json
            return json_resultado

        except openai.AuthenticationError as e:
            print(f"Erro de Autenticação: {e}")
        except openai.APIError as e:
            print(f"Erro na API: {e}")

    def gerar_parecer(self,transacao):
        print("2. Gerando um Parecer para cada transacao")
        prompt_sistema = f"""
        Para a seguinte transação, forneça um parecer, apenas se o status dela for de "Possível Fraude". Indique no parecer uma justificativa para que você identifique uma fraude.
        Transação: {transacao}

        ## Formato de Resposta
        "id": "id",
        "tipo": "crédito ou débito",
        "estabelecimento": "nome do estabelecimento",
        "horario": "horário da transação",
        "valor": "R$XX,XX",
        "nome_produto": "nome do produto",
        "localizacao": "cidade - estado (País)"
        "status": "",
        "parecer" : "Colocar Não Aplicável se o status for Aprovado"
        """
        lista_mensagens = [
            {
                "role": "user",
                "content": prompt_sistema
            }
        ]
        resposta = self.cliente.chat.completions.create(
            messages=lista_mensagens,
            model=self.modelo,
        )
        conteudo = resposta.choices[0].message.content
        print("Finalizou a geração de parecer")
        return conteudo

    def gerar_recomendacao(self,um_parecer):
        print("3. Gerando recomendações")

        prompt_sistema = f"""
        Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes da transação da Transação: {um_parecer}

        As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-Fraude" ou "Realizar Verificação Manual".
        Elas devem ser escrito no formato técnico.

        Inclua também uma classificação do tipo de fraude, se aplicável. 
        """

        lista_mensagens = [
            {
                "role": "system",
                "content": prompt_sistema
            }
        ]

        resposta = self.cliente.chat.completions.create(
            messages=lista_mensagens,
            model=self.modelo,
        )

        conteudo = resposta.choices[0].message.content
        print("Finalizou a geração de recomendação")
        return conteudo

    def estudo_inicial_transacoes(self,transacoes_analisadas):
        for uma_transacoes in transacoes_analisadas["transacoes"]:
            if uma_transacoes["status"] == "Possível Fraude":
                um_parecer = self.gerar_parecer(uma_transacoes)
                recomendacao = self.gerar_recomendacao(um_parecer)
                id_transacao = uma_transacoes["id"]
                produto_transacao = uma_transacoes["nome_produto"]
                status_transacao = uma_transacoes["status"]
                return self.salva_arquivo(f"./dados/trasacao{id_transacao}-{produto_transacao}-{status_transacao}.txt",recomendacao)



if __name__ =="__main__":
    gerar_transacoes = AnaliseTransacoes()
    lista_transacoes = gerar_transacoes.carrega("./dados/transacoes.csv")
    transacoes_analisadas = gerar_transacoes.analisa_transacao(lista_transacoes)
    gerar_lista = gerar_transacoes.estudo_inicial_transacoes(transacoes_analisadas)

