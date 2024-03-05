import pandas as pd
import numpy as np
from tqdm import tqdm
from utils import analyze_promo_v2
import time
import json
import sys


def get_promo_data(row, key):
    assert key in ['index', 'categorias_en_promo', 'marcas_en_promo', 'cuotas_sin_interes', 'cupon_app', 'promociones_envio',
                   'publico_objetivo', 'promocion', 'productos_en_oferta'], 'wrong key'

    if row == 'img loading problem':
        return np.nan

    row_dict = row[0]
    if row_dict != '':
        return row_dict[key]

    if row_dict == np.nan or row_dict == None:
        return np.nan

def main(argv):
    assert argv[1] in ['falabella', 'paris'], 'retails supported: falabella or paris as argv'
    # import df
    df = pd.read_csv(f'df_promos_retail_{argv[1]}.csv', index_col=0)
    print(df)
    print('analyzing...')
    start = time.time()
    df['promo_analysis'] = df['url_img'].apply(lambda row: analyze_promo_v2(row))
    # json to cols
    df['promocion'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='promocion'))
    df['publico_objetivo'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='publico_objetivo'))
    df['categorias_en_promo'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='categorias_en_promo'))
    df['marcas_en_promo'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='marcas_en_promo'))
    df['productos_en_oferta'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='productos_en_oferta'))
    df['cuotas_sin_interes'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='cuotas_sin_interes'))
    df['cupon_app'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='cupon_app'))
    df['promociones_envio'] = df['promo_analysis'].apply(lambda row: get_promo_data(row, key='promociones_envio'))
    df.drop(columns='promo_analysis', inplace=True)
    df.to_csv(f'df_promos_retail_analysis_{argv[1]}.csv')
    total = round(time.time() - start,2)
    print(f'time taken: {total} secs')

if __name__ == '__main__':
    main(sys.argv)
