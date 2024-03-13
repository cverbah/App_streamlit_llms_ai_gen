import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from unidecode import unidecode
import matplotlib
matplotlib.use('Agg')
import streamlit as st
import plotly.express as px


def plot_wordcloud(df, col, color='black', max_words=20, height=200):
    assert col in ['categorias_en_promo', 'marcas_en_promo', 'publico_objetivo'], 'wrong key'
    keywords = df[col].tolist()
    keywords_flatten = [val for sublist in keywords for val in sublist]
    keywords_flatten_format = list(map(lambda x: unidecode(x.lower()), keywords_flatten))
    keywords_promo_all_tokens = ' '.join(keywords_flatten_format)

    wordcloud = WordCloud(background_color=color, max_words=max_words, height=height).generate(keywords_promo_all_tokens)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    return plt


def plot_against_offer_type(df, col, top=10):
    assert col in ['categorias_en_promo', 'marcas_en_promo', 'publico_objetivo'], 'wrong key'
    keywords = df[col].tolist()
    keywords_flatten = [val for sublist in keywords for val in sublist]
    keywords_flatten_format = list(map(lambda x: unidecode(x.lower()), keywords_flatten))
    col_counter = Counter(keywords_flatten_format).most_common()[:top]
    df_counter = pd.DataFrame(col_counter, columns=[f'{col}', 'total'])
    df_counter = df_counter.sort_values(by='total', ascending=True)

    fig = px.bar(df_counter, x="total", y=f"{col}")
    return fig

        
