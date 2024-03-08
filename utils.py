import os
from dotenv import load_dotenv
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import VertexAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain_core.messages import HumanMessage
from PIL import Image
from serpapi import GoogleSearch
import json


# env
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'
GOOGLE_API_KEY = os.environ['GCP_API_KEY']
SERPAPI_API_KEY = os.environ['SERPAPI_API_KEY']  # https://serpapi.com/google-trends-api

# OpenAI Models
openai_model_3 = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY)
openai_model_4 = ChatOpenAI(temperature=0, model_name='gpt-4-turbo-preview', openai_api_key=OPENAI_API_KEY)
# GCP Model (Gemini Pro) v2
gcp_model = VertexAI(temperature=0, model_name="gemini-pro")
gcp_model_vision = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro-vision", google_api_key=GOOGLE_API_KEY)
gcp_model_txt = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro", google_api_key=GOOGLE_API_KEY)


def search_google_trends(query, data_type='RELATED_TOPICS', geo='CL'):
    assert data_type in ['RELATED_TOPICS', 'RELATED_QUERIES', 'GEO_MAP_0', 'GEO_MAP', 'TIMESERIES'], 'data_type not supported'
    params = {
        "engine": "google_trends",
        "q": query,
        "geo": geo,
        "data_type": data_type,
        "api_key": SERPAPI_API_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    #interest_over_time = results["interest_over_time"]
    return results


def analyze_promo_v4(img_data, promo_type, format=True, model=gcp_model_txt):
    '''' just testing for now : same example from gcp'''

    instructions = f"Instrucciones: La siguiente data corresponde a información relacionada a promociones de un retail de la competencia. \
                    Estas promociones están segmentadas como: {promo_type} del retail. \
                    Cada promoción cuenta con la siguiente información:\n \
                    - posición: número que refleja a la importancia de la promoción  \n \
                    - promoción: características principales de la promoción  \n \
                    - categorías: categorías de la promoción  \n \
                    - público objetivo: potenciales clientes a los que está dirigida la promoción  \n \
                    Extrae toda la información que puedas de las promociones y has un análisis general que contemple todas las promociones, dando \
                    una recomendación de que estrategias se podrían utilizar en mi retail sabiendo sobre estas promociones de la competencia. \
                    Se lo más analítico posible en tu análisis y recomendación"

    try:
        content_data = [{"type": "text",
                         "text": f"{instructions}"}]
        prompt_data = [({"type": "text", "text": f"- posición: {pos}\n \
                                                   - promoción: {promo}\n \
                                                   - categorías: {cat}\n \
                                                   - público objetivo: {target}"})
                        for pos, promo, cat, target in img_data]

        for pair_data in prompt_data:
            content_data.extend(pair_data)

        content_data.extend([{"type": "text",
                              "text": "Entrega la respuesta en formato json: [{'analysis': análisis general,\
                                       'recommendation': recomendación de estrategia para mi retail}"}])

        message = HumanMessage(
            content=content_data
        )
        response = model.invoke([message]).content

        if format:
            response = response.replace(' ```json\n', '').replace('\n```', '').replace('\n', '')
            response = json.loads(response)

        return response

    except Exception as e:
        print(e)
        return e

def analyze_promo_v3(img_data, promo_type, format=True, model=gcp_model_vision):
    '''' just testing for now : same example from gcp'''

    instructions = f"Instrucciones: Las siguientes imágenes contienen promociones de un retail competidor en donde la posición corresponde a la \
                    relevancia de la promoción. Estas promociones son las ofertas: {promo_type} del retail. \
                    Extrae toda la información que puedas de las promociones y has un análisis general que contemple todas las promociones, dando \
                    una recomendación de que estrategias se podrían utilizar en mi retail sabiendo sobre estas promociones de la competencia. \
                    Se lo más analítico posible en tu análisis y recomendación"

    try:
        content_data = [{"type": "text",
                         "text": f"{instructions}"}]
        prompt_data = [({"type": "text", "text": f"Esta imagén está en la posición {pos} y la promoción esta enfocada en {name}"},
                        {"type": "image_url", "image_url": img}) for img, pos, name in img_data]

        for pair_data in prompt_data:
            content_data.extend(pair_data)

        content_data.extend([{"type": "text",
                              "text": "Entrega la respuesta en formato json: [{'analysis': análisis general,\
                                       'recommendation': recomendación de estrategia para mi retail}"}])

        message = HumanMessage(
            content=content_data
        )
        response = model.invoke([message]).content

        if format:
            response = response.replace(' ```json\n', '').replace('\n```', '').replace('\n', '')
            response = json.loads(response)

        return response

    except Exception as e:
        print(e)
        return 'img loading problem'


def analyze_promo_v2(image_path, format=True, model=gcp_model_vision):
    '''' just testing for now : same example from gcp'''

    instructions = "Instrucciones: Las siguientes imágenes contienen promociones de retails, extrae información de las promociones.Solo usa la información" \
                   "disponible en las imágenes. Siempre respondes en español y en minúsculas."
    prompt = """
    Extrae la información siguiendo estos pasos y guardando la información en un archivo json siguiendo la siguiente estructura:
    [{'index': indice de imágen partiendo con 1}]
    Paso 1: Analiza las ofertas y promociones de manera general presentes en cada imágen, respondiendo las siguientes preguntas,
    agregando los datos al archivo json:\
    'categorias_en_promo': Sobre qué categorías trata la promoción? Usa siempre 3 palabaras claves y almacénalas en una lista.  
    'marcas_en_promo': Qué marcas están con promoción? Almacena todas las marcas detectadas en una lista. Si no hay, devuelve null.
    'duracion_promo': [{'fecha_inicio_promo': fecha inicio promoción con el siguiente formato de fecha: dd/mm/aaaa,
                        'fecha_termino_promo: fecha termino promoción con el siguiente formato de fecha: dd/mm/aaaa,
                        'dias_duracion': días que dura la promoción con formato: int}]. Si no hay fechas, devuelve null.
    'cuotas_sin_interes': Es posible comprar en cuotas sin interés? Si es que sí, cuantas cuotas? en formato: int. Si no detectas la palabra cuota, devuelve null.
    'cupon_app': Hay cupones de descuento usando sólo la app del retail? Si es que hay, extrae la información. Si no hay, devuelve null.
    'promociones_envio': Hay promociones para el envío?  Si es que hay, describe la promoción. Si no hay, devuelve null.
    'publico_objetivo': Cual crees que es el público objetivo de esta promoción?
                        Devuelve 5 adjetivos calificativos del público objetivo  y almacénalas en una lista. Usa 1 palabra para representar cada característica.
    [{'promocion': analisis del paso 1 y de la promoción principal de la imágen. Nunca inventes datos si no aparecen en la imágen.}]
    Paso 2: Identifica cuantos productos con precios con descuentos hay en la imagen, mostrando el precio sin y con descuento.
            Si no sale el precio de cada producto de forma explícita, no guardes la información.
    Paso 3: Extra la información de cada producto siempre y cuando tenga descuentos y agregala al archivo json siguiendo la siguiente estructura:\
    ['productos_en_oferta': [{'nombre_del_producto': nombre completo del producto,
                              'precio_normal': precio normal,
                              'precio_oferta': precio oferta,
                              'descuento': descuento formateado con porcentaje]}]
    Si no logras detectar productos específicos con precios con descuento en la imagen, devuelve la lista vacía.
    Considera siempre todos los 0 en los precios de los productos.
    Paso 4: Si no es posible extraer ciertos datos de la imagen, guardar el dato como null
    Paso 5: Formatea el archivo. Elimina caractéres especiales si es necesario.
    """
    try:
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": f"{instructions}",
                },
                {"type": "image_url",
                 "image_url": image_path},
                {"type": "text",
                 "text": prompt},
            ]
        )
        response = model.invoke([message]).content

        if format:
            response = response.replace(' ```json\n', '').replace('\n```', '').replace('\n', '')
            response = json.loads(response)

        return response

    except Exception as e:
        print(e)
        return 'img loading problem'


def analyze_promo(image_path, model=gcp_model_vision):

    prompt = 'Extract all the relevant data from the the image and return it with a json format. Only use the data from the image. Image:'
    prompt2 = ''

    message = HumanMessage(
        content=[
            {
             "type": "text",
             "text": f"{prompt}",
            },
            {"type": "image_url",
             "image_url": image_path}
        ]
    )
    response = model.invoke([message]).content
    return response

def analyze_image(image_path, model=gcp_model_vision, analyst_type=1):
    assert analyst_type in ([1, 2, 3]), 'analyst_type must be in [1,2,3]'

    if analyst_type:
        prompt = 'Que puedes decir acerca de la imágen? Se específico y detallado. Siempre respondes en español.'

    if analyst_type == 2:
        prompt = 'Haz un análisis del siguiente gráfico o tabla. Actúa como un experto en ciencia de datos. Siempre respondes en español.'

    if analyst_type == 3:
        prompt = 'Extract all the relevant data from the the image and return it with a json format. Only use the data from the image.'

    message = HumanMessage(
        content=[
            {
             "type": "text",
             "text": f"{prompt}",
            },  # You can optionally provide text parts
            {"type": "image_url",
             "image_url": image_path}
        ]
    )
    response = model.invoke([message]).content
    return response


def pandas_agent_func(df, user_message, model='gcp', steps=True): #callback,
    try:
        if model == 'gcp':
            model = gcp_model
            agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION
        else:
            model = openai_model_3
            agent = AgentType.OPENAI_FUNCTIONS

        agent = create_pandas_dataframe_agent(
            model,
            df,
            verbose=True,
            agent_type=agent,
            handle_parsing_errors=True,
            return_intermediate_steps=steps,
        )
        tool_input = {
            "input": {
                "name": "python",
                "arguments": f'{user_message}. Always speak in spanish'
            }
        }
        if steps:
            response = agent(tool_input) #, callbacks=[callback]
            return response

        response = agent.run(tool_input) #, callbacks=[callback]
        return response

    except Exception as e:
        print(f"Error: {e}")
        return None


def format_pricing_table(df):
    df = df.iloc[:, :9]
    df.columns = (df.columns.
                  str.replace(' ', '_').
                  str.lower().
                  str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    df['sku'] = df['sku'].astype(str)
    df['mas_bajo'] = df['mas_bajo'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    df['mas_alto'] = df['mas_alto'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    df['precio_mercado'] = df['precio_mercado'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    df['precio_de_lista'] = df['precio_de_lista'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    df = df.reset_index(drop=True)
    return df

def format_compete_table(df):
    df.columns = (df.columns.
                  str.replace(' ', '_').
                  str.lower().
                  str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    df['sku_tienda'] = df['sku_tienda'].astype(str)
    df['fecha'] = pd.to_datetime(df['fecha'])
    #df['precio_normal'] = df['precio_normal'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    #df['precio_final'] = df['precio_final'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))
    #df['precio_tarjeta'] = df['precio_tarjeta'].apply(lambda row: int(row.replace('$ ', '').replace(',', '')))

    df = df.reset_index(drop=True)
    return df
