# -*- coding: utf-8 -*-

from pymongo import MongoClient
import datetime
import pprint

# Conexão com o MongoClient.
client = MongoClient('localhost', 27017)
# Obtendo um banco de dados.
db = client.gran_turismo_sport
# Obtendo uma coleção.
posts = db.carros

# Usando um dicionários para representar um documento.
post1 = {"carro": {
            "data": {
                "modelo": "V8 Vantage S '15",
                "construtor": "Aston Martin",
                "pais": "Reino Unido",
                "categoria": "N400",
                "potencia_max_cv": 449,
                "potencia_max_rpm": 7100,
                "torque_max_mkgf": 51.4,
                "torque_max_rpm": 5000,
                "tracao": "FR",
                "aspiracao": "Aspirado",
                "cilindrada_cc": 4735,
                "comprimento_mm": 4385,
                "largura_mm": 2022,
                "altura_mm": 1260,
                "peso_kg": 1610,
                "ano": 2015
            },
            "desempenho": {
                "velocidade_max": 8.0,
                "aceleracao": 4.3,
                "freio": 2.2,
                "curva": 2.0,
                "estabilidade": 5.1
            },
            "status": {
                "distancia_percorrida": 11.3,
                "alteracao": 1,
                "numero_corridas": 0,
                "numero_vitorias": 0,
                "valor_real": 180000
            }
        }}

post2 = {"carro": {
            "data": {
                "modelo": "Mustang GT Premium Fastback '15",
                "construtor": "Ford",
                "pais": "Estados Unidos",
                "categoria": "N400",
                "potencia_max_cv": 441,
                "potencia_max_rpm": 6500,
                "torque_max_mkgf": 55.3,
                "torque_max_rpm": 4500,
                "tracao": "FR",
                "aspiracao": "Aspirado",
                "cilindrada_cc": 0,
                "comprimento_mm": 4783,
                "largura_mm": 1915,
                "altura_mm": 1382,
                "peso_kg": 1681,
                "ano": 2015
            },
            "desempenho": {
                "velocidade_max": 6.7,
                "aceleracao": 3.4,
                "freio": 2.2,
                "curva": 1.9,
                "estabilidade": 4.7
            },
            "status": {
                "distancia_percorrida": 11.5,
                "alteracao": 2,
                "numero_corridas": 0,
                "numero_vitorias": 0,
                "valor_real": 44310
            }
        }}


# Para inserir um documento: (post), em uma coleção: (posts [db.carros]).
post_id1 = posts.insert_one(post1).inserted_id
post_id2 = posts.insert_one(post2).inserted_id
print(post_id1)
print(post_id2)
print("...")
