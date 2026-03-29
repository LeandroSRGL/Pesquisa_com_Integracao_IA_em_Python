# 📄 Pesquisa com Integração IA
Responde perguntas acadêmicas e gera um PDF formatado.

## Funcionalidades
- Fazer perguntas acadêmicas diretamente no terminal
- Respostas objetivas com linguagem acadêmica e fontes confiáveis
- Geração automática de PDF para cada resposta

## Como funciona
Você digita uma pergunta, a IA responde e o PDF é salvo automaticamente na pasta `PDFs/` com o nome baseado na pergunta.
```
Digite sua pergunta: O que é fotossíntese?
PDF Gerado!
Ele gera: O_que_e_fotossintese.pdf
Quer fazer outra pergunta? Y ou N:
```

## Requisitos
- Python 3.8+
- `groq` `python-dotenv` `reportlab`
- API Key da GROQ no arquivo `.env`

> ⚠️ **O projeto não funciona sem a API Key da Groq.** Crie um arquivo `.env` na raiz do projeto com:
> ```
> GROQ_API_KEY=#suakeyaqui
> ```
