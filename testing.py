from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain import LLMChain
from dotenv import load_dotenv
import os
import pandas as pd

#load env
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def main():
    try:
        # Read uploaded file into a DataFrame
        df = pd.read_csv('Purina Specialty - Catálogo de match_csv.csv')

    except Exception as e:
        print(e)

    # cooking
    df = df.iloc[:, :9].head(10)
    df.columns = (df.columns.
                  str.replace(' ', '_').
                  str.lower().
                  str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    df['sku'] = df['sku'].astype(str)
    df['mas_bajo'] = df['mas_bajo'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    df['mas_alto'] = df['mas_alto'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    df['precio_mercado'] = df['precio_mercado'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    df['precio_de_lista'] = df['precio_de_lista'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))

    chat = ChatOpenAI(temperature=0, model_name='gpt-4-turbo-preview', openai_api_key=OPENAI_API_KEY)
    template = (
        "You are a helpful and experienced data analyst that speaks in {input_language}. Given the {df} given by the user, provide valuable insights.\
         If you cannot find the answer of a given question in the data provided, answer that there is not enough data to answer the question"
     )
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
     )

    response = str(chat(
                    chat_prompt.format_prompt(
                    input_language="Spanish", df=df,
                    text=f"Hazme un listado de los 10 productos más baratos separados por 'categoria' y usando el precio: 'precio_de_lista'"
                     ).to_messages()
                ).content)

    print(response)

if __name__ == "__main__":

    main()