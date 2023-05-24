from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from textblob import TextBlob
from textblob.exceptions import NotTranslated

from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv(find_dotenv())


def translate_to_english(text):
    try:
        tb = TextBlob(text)
        translated = tb.translate(to='en')
        return str(translated)

    except NotTranslated:
        return text

def analyze_sentiment_pt(text):
    # Traduzindo o texto para inglês
    text_en = translate_to_english(text)

    # Análise de sentimento com TextBlob
    testimonial = TextBlob(text_en)
    polarity = testimonial.sentiment.polarity

    # Retornando o sentimento
    if polarity < 0:
        return 'negativo'
    elif polarity > 0:
        return 'positivo'
    else:
        return 'neutro'


def draft_email(user_input, name="Fabio"):
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)

    template = """
    
 Você é um assistente prestativo que elabora um rascunho de resposta de e-mail com base em um novo e-mail. Você também pode responder mensagens de Whatsapp e Facebook. 

 Seu objetivo é ajudar o usuário a criar rapidamente uma resposta de e-mail perfeita.

 Mantenha sua resposta curta e direta e imite o estilo do e-mail, respondendo de maneira semelhante para combinar com o tom.

 Comece sua resposta dizendo: "Olá {name}, aqui está um rascunho para sua resposta:". E então continue com a resposta em uma nova linha.

 ertifique-se de terminar com {signature}.
    
    """

    signature = f"Atenciosamente, \n\{Fabio}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "Aqui está o e-mail para responder e considere quaisquer outros comentários do usuário para a resposta também: {user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(user_input=user_input, signature=signature, name=name)

    return response
