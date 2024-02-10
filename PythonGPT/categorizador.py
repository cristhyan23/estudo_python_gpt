from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
#Acessa o diretório e captura a API Key
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-3.5-turbo-0125"

categorias = """
                Transporte de carga terrestre,
                Transporte de carga aérea,
                Transporte de carga marítima,
                Gestão de frota,
                Armazenagem de produtos,
                Gestão de inventário,
                Distribuição de produtos,
                Monitoramento de mercadorias em trânsito,
                Embalagem de produtos,
                Roteirização de entregas,
                Gestão de Armazéns,
                Gestão de fornecedores,
                Gestão de contratos logísticos,
                Processamento de pedidos,
                Armazenamento de informações logísticas,
                Tecnologia da informação aplicada à logística,
                Manutenção de equipamentos logísticos,
                Gestão de devoluções,
                Sistemas de gerenciamento de transporte (TMS),
                Sistemas de gerenciamento de armazéns (WMS),
                Auditoria logística,
                Documentação aduaneira,
                Classificação fiscal de produtos,
                Compliance regulatório internacional,
                Gestão de riscos em transações internacionais,
                Estratégias de precificação para exportação,
                Logística de frete internacional,
                Embalagem para transporte internacional,
                Seguro de carga internacional,
                Rastreamento de carga em operações internacionais,
                Acordos e termos de comércio internacional,
                Seguros,
                Gerenciamento de Ricos,
                Atendimento ao Cliente,
                Engenharia Logística
"""
def tira_duvidas_e_categoriza_termos_logistico(item,categoria):
    prompt_sistema = f"""
                Você é um categorizador de itens relacionados a logística
                Você deve assumir as categorias presentes na lista abaixo:
                #Lista de Categorias Válidas
                {categoria.split(",")}
                #Formato Saída
                Pergunta: Descrição da Pergunta feita
                Categoria: apresente a categoria do item
                Descrição: Detalhe um resumo sobre o item e a relação com a categoria
                """
    resposta = cliente.chat.completions.create(
        messages = [
            {
                "role": "system",
                "content":prompt_sistema
            },
            {"role": "user",
                "content": item}
        ],
        model =modelo,
        temperature = 1,
        max_tokens=200
    )

    return resposta.choices[0].message.content
def valida_se_usuario_deseja_continuar_com_as_perguntas():
   while True:
        try:
            validar_continuacao = input("Deseja fazer mais alguma pergunta? ( Y | N ) ")
            if validar_continuacao.upper() != 'N' and validar_continuacao.upper() != 'Y':
                raise ValueError("Digite somente Y ou N")
            elif validar_continuacao.upper() == 'N':
                return False
            elif validar_continuacao.upper() == 'Y':
                return True
        except ValueError as e:
            print(e)
def executa_fluxo_de_perguntas():
    while True:
        item_logistica = input("Digite o tema que está em dúvida: ")
        texto_resposta = tira_duvidas_e_categoriza_termos_logistico(item_logistica, categorias)
        print(texto_resposta)
        check_continuacao = valida_se_usuario_deseja_continuar_com_as_perguntas()
        if check_continuacao != True:
            break

if __name__ == "__main__":
    executa_fluxo_de_perguntas()