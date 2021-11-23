from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
import requests
import json

app = Flask(__name__)
api = Api(app)

df = pd.read_csv('https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/dados-ba-4.csv')
df.to_csv('produtos.csv', index=False)

df_produtos = pd.read_csv('produtos.csv')

df_produtos = pd.read_csv('produtos.csv')

produto_principal_marketing = df_produtos['id'] == 488
df_produtos[produto_principal_marketing]

class Produto(Resource):
    def get(self, produto_id):
        produto_procurado = df_produtos['id'] == produto_id
        produto = df_produtos[produto_procurado]
        return produto.to_json()

    def post(self, produto_id):
        dados = request.form['data']
        print(produto_id, dados)
        return produto.to_json()

api.add_resource(Produto, '/produtos/<int:produto_id>')

if __name__ == '__main__':
    app.run(debug=True)