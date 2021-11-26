from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt

def ler_base():
    # df = pd.read_csv('https://raw.githubusercontent.com/erlon-wandenkolk/ProjetoApi_letscode_mod2/main/TA_PRECO_MEDICAMENTO.csv',sep=';',error_bad_lines=False,encoding="ISO-8859-1")
    # df.to_csv('base_medicamentos.csv', index=False)
    df = pd.read_csv('base_medicamentos.csv',thousands='.',decimal=',')
    return df

def limpar_base(df):
    eliminar_estes = ['CNPJ', 'LABORATÓRIO', 'CÓDIGO GGREM', 'REGISTRO',
           'EAN 1', 'EAN 2', 'EAN 3', 'APRESENTAÇÃO',
           'CLASSE TERAPÊUTICA', 'TIPO DE PRODUTO (STATUS DO PRODUTO)',
           'REGIME DE PREÇO', 'PF 12%', 'PF 17%',
           'PF 17% ALC', 'PF 17,5%', 'PF 17,5% ALC', 'PF 18% ALC',
           'PMC 12%', 'PMC 17%', 'PMC 17% ALC', 'PMC 17,5%',
           'PMC 17,5% ALC', 'PMC 18% ALC', 'CAP', 'CONFAZ 87', 'ICMS 0%',
           'ANÁLISE RECURSAL',
           'LISTA DE CONCESSÃO DE CRÉDITO TRIBUTÁRIO (PIS/COFINS)',
           'TARJA']

    df.drop(eliminar_estes,inplace=True,axis=1)
    return df

def filtrar_base(df):
    filtro = (df['RESTRIÇÃO HOSPITALAR'] == 'Não') & (df['COMERCIALIZAÇÃO 2020'] == 'Sim')
    return df[filtro]

def criar_groupby(df):
    meu_groupby = df.groupby('SUBSTÂNCIA').agg({'PF 0%':'mean',
                             'PMC 0%':'mean', } ,index=True)
    meu_groupby['Est. Med. Margem Lucro %'] = (meu_groupby['PMC 0%']/meu_groupby['PF 0%']-1)*100

    return meu_groupby

def criar_figura(df_groupby):
    filtro = (df_groupby['Est. Med. Margem Lucro %'] > 0) & (df_groupby['Est. Med. Margem Lucro %'] < 200)
    df_imagem = df_groupby[filtro].plot(y='Est. Med. Margem Lucro %')
    plt.savefig('grafico.jpeg')



app = Flask(__name__)
api = Api(app)

df = ler_base()
limpar_base(df)
df = filtrar_base(df)

class Medicamento(Resource):
    df = ler_base()
    limpar_base(df)
    df = filtrar_base(df)

    def get(self):
       return df.to_json()

class Agrupamento(Resource):
    df = ler_base()
    limpar_base(df)
    df = filtrar_base(df)
    group_by = criar_groupby(df)

    def get(self,tipo):
        group_by = criar_groupby(df)
        if tipo == 0:
            group_by.to_csv('agrupamento.csv')
            return group_by.to_csv()
        if tipo == 1:
            group_by.to_json('agrupamento.json')
            return group_by.to_json()
        if tipo == 2:
            return criar_figura(group_by)

api.add_resource(Medicamento, '/medicamentos')
api.add_resource(Agrupamento, '/agrupar/<int:tipo>')

if __name__ == '__main__':
    app.run(debug=True)