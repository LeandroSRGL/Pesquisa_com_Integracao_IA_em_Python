import os #Importa o sistema
from dotenv import load_dotenv #Importa o dotenv
import re #Importa o modulo de expressões regulares

from reportlab.platypus import SimpleDocTemplate, Paragraph #SimpleDocTemplate = estrutura base do PDF; Paragraph = bloco de texto formatado
from reportlab.lib.pagesizes import A4 #Importa a variavel que define o tamanho da página A4
from reportlab.lib.styles import ParagraphStyle #Criar estilos personalizados

from groq import Groq #Importa a IA

load_dotenv() #Carrega o dotenv
client = Groq(api_key=os.getenv('GROQ_API_KEY')) #O agente IA pede uma APIKey conectada a conta, aqui ela pega no .env

def genPDF(output, path, pergunta): #Função para gerar pdf

        '''
        Parametros:
           output: resposta da IA
           path: caminho que vai ser salvo o PDF
           pergunta: pergunta do usuario'''

        batata = ParagraphStyle( #Cria um estilo de formatação para os paragrafos
            'batata', #Nome do estilo
            fontSize=12, #Tamanho da fonte
            fontName='Helvetica', #Fonte usada
            leading=16, #Espaçamento entre as linhas
            spaceAfter=10, #Espaçamento depois do parágrafo
        )

        batata2 = ParagraphStyle( #Cria um estilo de formatação para as fontes
            'batata2', #Nome do estilo
            fontSize=10, #Tamanho da fonte
            fontName='Helvetica-BoldOblique', #Fonte usada
            leading=16, #Espaçamento entre as linhas
            spaceAfter=10, #Espaçamento depois do parágrafo
        )

        batata3 = ParagraphStyle( #Cria um estilo de formatação para o titulo
            'batata3', #Nome do estilo
            fontSize=16, #Tamanho da fonte
            fontName='Helvetica-Bold', #Fonte usada
            leading=22, #Espaçamento entre as linhas
            spaceAfter=10, #Espaçamento depois do parágrafo
            alignment=1, #Alinhar no centro do documento
        )

        template = SimpleDocTemplate(path, pagesize=A4) #Define o caminho onde será salvo o PDF e qual o tamanho da página usada
        conteudo = [] #Cria uma lista

        conteudo.append(Paragraph(pergunta, batata3)) #Cria o titulo(pergunta)

        for paragrafo in output.split('\n')[:-1]: #Divide o output em linhas, pega todas menos a ultima
            if paragrafo != '': #Verifica se não é uma string vazia
                conteudo.append(Paragraph(paragrafo, batata)) #Cria um parágrafo e adiciona na lista conteudo

        fontes = output.split('\n')[-1] #Divide o output em linhas, pega somente a ultima
        for fonte in fontes.split(';'): #Divide as fontes pelo ;
            if fonte != '': #Verifica se não é uma string vazia
                conteudo.append(Paragraph(fonte, batata2)) #Cria um parágrafo e adiciona na lista conteudo

        template.build(conteudo) #Pega tudo que esta na lista conteudo e gera o PDF

while True: #Loop para perguntas sequenciais

    pergunta = input("Digite sua pergunta: ") #Pega o input do usuario

    resposta = client.chat.completions.create(
        model="groq/compound-mini",
        messages=[
            {"role": "system", "content": "Você é um assistente acadêmico especializado em pesquisa científica, produção de conteúdo educacional e apoio a estudos universitários. Seu objetivo é fornecer informações diretas, objetivas, verificáveis, atualizadas e fundamentadas em fontes confiáveis. É proibido usar Wikipédia como fonte. Priorize fontes oficiais, científicas e institucionais, dando preferência a sites brasileiros, como portais governamentais (.gov.br), universidades públicas brasileiras, institutos de pesquisa, revistas científicas e bases acadêmicas reconhecidas. As informações devem ser atuais e verificáveis. As respostas devem ser claras, técnicas, objetivas, bem estruturadas, sem conteúdo especulativo, genérico ou sem base científica, com linguagem acadêmica e sem informalidade. O formato da resposta deve ser organizado, com dados objetivos, conceitos bem definidos e sem opiniões pessoais. Ao final da resposta, é obrigatório informar as fontes utilizadas com nome da instituição ou site, quando aplicável. A resposta deve ser em texto puro, sem nenhuma formatação markdown, sem asteriscos, sem tabelas, sem traços, sem tags HTML como br, sem títulos com cerquilha e sem qualquer outro caractere especial de formatação. Use apenas texto corrido com parágrafos simples. Não quero links nas fontes, somente as citações. Sempre separar as fontes por ';' "},
            {"role": "user", "content": pergunta}
        ]
    ) #Integração com a IA

    output = resposta.choices[0].message.content #Pega a resposta que a IA mandou
    output = output.replace('‑', '-').replace('–', '-').replace('"', '"').replace('"', '"') #Substitui alguns caracteres que a IA manda, que não são aceitos
    dir = os.path.dirname(os.path.abspath(__file__)) #Pega o diretorio onde esta o .py
    os.makedirs(os.path.join(dir, 'PDFs'), exist_ok=True) #Cria uma pasta para os PDFs
    path = os.path.join(dir, 'PDFs/' + re.sub(r'[^\w\s]', '', pergunta).replace(' ', '_') + '.pdf') #Especifica o caminho que o PDF deve ser criado e remove qualquer caractere especial, tambem substitui espaço por "_"

    genPDF(output, path, pergunta) #Chama a função de gerar PDF
    print("PDF Gerado!") #Avisa que o PDF foi gerado

    continua = input("Quer fazer outra pergunta? Y ou N: ") #Manda outro input para o usuario
    if continua.upper() == 'N': #Verifica se o usuario quer ou não fazer outra pergunta
         break #Quebra o loop