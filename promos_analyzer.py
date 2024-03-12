import pandas as pd
import numpy as np
from tqdm import tqdm
from utils import analyze_promo_v2
import time
import json
import sys
import re


def get_promo_data(row, key):
    assert key in ['index', 'categorias_en_promo', 'marcas_en_promo', 'cuotas_sin_interes', 'cupon_app', 'promociones_envio',
                   'publico_objetivo', 'promocion', 'productos_en_oferta', 'duracion_promo'], 'wrong key'

    if row == 'img loading problem':
        return np.nan

    row_dict = row[0]
    if row_dict != '':
        return row_dict[key]

    if row_dict == np.nan or row_dict == None:
        return np.nan


def extract_discount(string):
    pattern = r'\b\d+(?:\.\d+)?%'
    discounts = re.findall(pattern, string)
    if discounts:

        discounts_float = list(map(lambda d: float(d.strip('%')) / 100, discounts))
        return discounts_float[0] #por ahora entrega el primero que encuentra
    else:
        return np.nan


def format_as_percentage(value):
    if pd.isnull(value):
        return np.nan
    else:
        return f"{value:.0%}"


def main(argv):
    assert argv[1] in ['falabella', 'paris', 'lider-supermercado', 'lider-catalogo', 'jumbo'],\
        'retails supported: falabella, paris, lider-supermercado, lider-catalogo, jumbo as argv'
    # import df
    df = pd.read_csv(f'./data_retails/promos_home/df_promos_retail_{argv[1]}.csv', index_col=0)
    print(df)
    print('analyzing...')
    start = time.time()
    df['promo_analysis'] = df['url_img'].apply(lambda row: analyze_promo_v2(row))
    # json to cols
    df['descripcion_promo'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='promocion'))
    df['duracion_promo'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='duracion_promo'))
    df['descuentos_promo'] = df['descripcion_promo'].apply(lambda row: extract_discount(str(row)))
    df['descuentos_promo'] = df['descuentos_promo'].apply(lambda row: format_as_percentage(row))
    df['categorias_en_promo'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='categorias_en_promo'))
    df['marcas_en_promo'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='marcas_en_promo'))
    df['publico_objetivo'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='publico_objetivo'))
    df['productos_en_oferta'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='productos_en_oferta'))
    df['cuotas_sin_interes'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='cuotas_sin_interes'))
    df['cupon_app'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='cupon_app'))
    df['promociones_envio'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='promociones_envio'))
    df.drop(columns='promo_analysis', inplace=True)
    df.to_csv(f'./data_retails/promos_home_analysis/df_promos_retail_analysis_{argv[1]}.csv')
    total = round(time.time() - start,2)
    print(f'time taken: {total} secs')

if __name__ == '__main__':
    main(sys.argv)
