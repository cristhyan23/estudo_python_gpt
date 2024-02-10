import tiktoken
import fitz # PyMuPDF LEITOR DE PDF

modelo = 'gpt-4'
codificador = tiktoken.encoding_for_model(modelo)
#CODIGO PARA EFETUAR LEITURA DE UM PDF

caminho_arquivo = 'C:\\Users\\SAMSUNG\Downloads\\ITB.BRA-M130 Extensão de deadline ao armador - CNC[2].pdf'
with fitz.open(caminho_arquivo) as documento_pdf:
    # Extrai o texto de todas as páginas do PDF
    texto = ""
    for pagina_num in range(documento_pdf.page_count):
        pagina = documento_pdf[pagina_num]
        texto += pagina.get_text()


#GERA UM CODIFICADOR PARA TRANSFORMAR O TEXTO EM EM TOKEN
lista_tokens = codificador.encode(texto)
print(f"Lista de Tokens:{lista_tokens} ")
print(f'Quantos Token Temos: {len(lista_tokens)}')
print(f'Custo para Modelo: {modelo} é de ${(len(lista_tokens)/1000) * 0.03} ')

modelo = 'gpt-3.5-turbo-0125'
codificador = tiktoken.encoding_for_model(modelo)
lista_tokens = codificador.encode(texto)

print(f"Lista de Tokens:{lista_tokens} ")
print(f'Quantos Token Temos: {len(lista_tokens)}')
print(f'Custo para Modelo: {modelo} é de ${(len(lista_tokens)/1000) * 0.0015} ')

# código omitido
print(f"O custo do GPT-4 é de {0.03/0.0015} maior que o do GPT-3.5 Turbo")
