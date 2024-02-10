import openai
from base_execucao_analise import ExecutadorAnalise

class AnaliseSentimento(ExecutadorAnalise):

    def __init__(self):
        super().__init__()

    def analisador_de_sentimentos(self,produto):
        prompt_sistema = f"""
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e depois, atribua qual o sentimento geral do produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.
        
        #Formato Saída:
        
        Nome do Produto: 
        Resumo das Avaliações:
        Sentimento Geral: [utilize apenas Positivo, Negativo ou Neutro]
        Pontos Fortes: lista com três bullets
        Pontos Fracos: lista com três bullets
        """

        prompt_usuario = self.carrega(f"./dados/avaliacoes-{produto}.txt")
        print(f"Iniciou analise de sentimentos dos {produto}")

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
                model=self.modelo
            )
            texto_resposta = resposta.choices[0].message.content
            self.salva_arquivo(f"./dados/analise-{produto}.txt",texto_resposta)

        except openai.AuthenticationError as e:
            print(f"Erro de Autenticação: {e}")
        except openai.APIError as e:
            print(f"Erro na API: {e}")

if __name__ == "__main__":
    sentimento = AnaliseSentimento()
    lista_produtos = ["Maquiagem mineral","Camisetas de algodão orgânico","Jeans feitos com materiais reciclados"]
    for produtos in lista_produtos:
        sentimento.analisador_de_sentimentos(produtos)
