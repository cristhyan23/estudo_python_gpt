from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
#Acessa o diretório e captura a API Key
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
resposta = cliente.chat.completions.create(
    messages = [
        {
            "role": "system",
            "content":"Atue como um especialista em logística internacional"
        },
        {"role": "user",
            "content":"Liste os tipos de modais possiveis para operar uma exportação"}
    ],
    model ="gpt-3.5-turbo"
)

print(resposta.choices[0].message.content)