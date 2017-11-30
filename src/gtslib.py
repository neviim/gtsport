# -*- coding: utf-8 -*-
# Neviim - 2017
# V-0.1.1

from pymongo import MongoClient
import pymongo
import json
import pprint
#
from gtsmath import GtsCalculos


class StatusCarro(object):
    """docstring for StatusCarro."""
    def __init__(self):
        super(StatusCarro, self).__init__()
        self.idcarro = 0
        self.extensao = '.json'
        self.path = '../data'

    def ler_dados_unico(self, arquivo):
        ''' abre um determinado arquivo txt em json, com os dados do carro,
            este deve ser uma unica estrutura com dados de um unico carro.

            Uso:
                statusCarro = StatusCarro()
                statusCarro.ler_dados_nunico()
        '''
        # abre o arquivo e o retorna como um dicionario.
        with open(self.path +'/'+ arquivo + self.extensao) as json_file:
            dados_carro = json.load(json_file)
        return dados_carro


class GranTurismoSport(object):
    """docstring para GranTurismoSport
            Uso:
                gtSport = GranTurismoSport()
    """
    def __init__(self, server='localhost', port=27017):
        super(GranTurismoSport, self).__init__()
        self.server = server
        self.port = port

        # Abre uma Collection do DataBase GranTurismoSport.
        clientdb = MongoClient(server, port)
        db = clientdb.GranTurismoSport

        # Se não existir o index ele sera criado.
        #if !exists(db.collection.exists("idkey")) {
        db.carros.create_index('idkey', unique=True)
        #}

        # Colesão de carros
        self.carros = db.carros

    def gera_md5(self, string1, string2):
        """ recebe duas string e retorna um codigo unico MD5.
                - Parametro:
                    string1 = qualquer valor string
                    string2 = qualquer valor string diferente da primeira

                - Uso:
                    gtSport = GranTurismoSport()
                    idkey = gtSport.gera_md5(string1, string2)

                - Retorno:
                    retorna um valor unico md5 semelhante a este formato,
                    '18e01c02fac56c795d6eab7a36b08bc5', valor este gerado
                    pela combinação da string1, string2 e uma key: neviim.
        """
        #string1 = "Mustang GT Premium Fastback '15"
        #string2 = "N400"
        mpwd = hashlib.md5(string1.encode())
        apwd = mpwd.hexdigest()
        codigo  = string2+"neviim"+apwd
        idcarro = hashlib.md5(codigo.encode())
        return idcarro.hexdigest()

    def cadastra_carro(self, gts):
        """ cadastra o os dados pasado por parametro no dicionario carro
                - Parametros:
                    carro => dicionario com os dados do carro a ser cadastrado.

                - Uso:
                    granturismosport = GranTurismoSport()
                    granturismosport.cadastro_carro(<status_carro_json>)

                - Dependencia:
                    Obrigatoriamente os campos chaves usado abaxo precisa constar
                    no arquivo json fornecido, [carro, data, modelo, categoria],
                    caso ele seja alterado, esta função não funcionara corretamente.

        """
        id_md5 = self.gera_md5(gts['carro']['data']['modelo'], \
                               gts['carro']['data']['categoria'])
        #
        gts['idkey'] = id_md5
        # efetua o cadastro somente caso este doc não esteja inserido.
        #print(self.carros.find({'idkey': id_md5}).count())
        if self.carros.find({'idkey': id_md5}).count() == 0:
            id_carro = self.carros.insert_one(gts).inserted_id
            print ("IDmdb: " + str(id_carro))
            print ("IDkey: " + str(id_md5))
            return True
        return False

    def get_categoria(self, categoria):
        """ procura por categoria
                - Parametros:
                    categoria => categoria do carro

                - Uso:
                    from gtslib import GranTurismoSport

                    gtSport = GranTurismoSport()
                    gts_carros_categoria = gtSport.get_categoria('N400')

                    # lista todos os carros da categoria espesificada.
                    for carro in gts_carros_categoria:
                        pprint.pprint(carro)

                - Retorno:
                    retorna uma lista com todos os carros na categoria especificada.
        """
        return self.carros.find({'carro.data.categoria': categoria})


if __name__ == '__main__':
    # usando a classe sobre dados do carro.
    #statusCarro = StatusCarro()
    #dados = statusCarro.ler_dados_unico('dados_carro')
    #print(dados)

    # biblioteca de algoritimos
    gtsCalculos = GtsCalculos()

    # get_categoria
    gtSport = GranTurismoSport('172.13.12.125')
    gts_carros_categoria = gtSport.get_categoria('N400')

    # vetor com todos os dados precessados que forao encontrado por filtro categoria.
    vetor_master = []

    # todos os carros da categoria espesificada em formato json.
    for item in gts_carros_categoria:
        # pprint.pprint(carro)
        # monta matrix com valores para calculos de IA
        vetor_potencia = []
        vetor_desempenho = []

        # monta vetor com os dados de potencia e torque.
        vetor_potencia.append(item['carro']['data']['potencia_max_cv'])
        vetor_potencia.append(item['carro']['data']['potencia_max_rpm'])
        vetor_potencia.append(item['carro']['data']['torque_max_mkgf'])
        vetor_potencia.append(item['carro']['data']['torque_max_rpm'])
        # monta vetor com os dados de
        vetor_desempenho.append(item['carro']['desempenho']['velocidade_max'])
        vetor_desempenho.append(item['carro']['desempenho']['aceleracao'])
        vetor_desempenho.append(item['carro']['desempenho']['freio'])
        vetor_desempenho.append(item['carro']['desempenho']['curva'])
        vetor_desempenho.append(item['carro']['desempenho']['estabilidade'])

        # monta vetor master
        """ [ [449, 7100, 51.4, 5000],
              [8.0, 4.3, 2.2, 2.0, 5.1],
              'bb3fb9ccde68f8e525dd563abf8d0a72',
              "V8 Vantage S '15"
            ] """
        # adiociona ao estrutura ao vetor master.
        vetor_master.append([vetor_potencia, vetor_desempenho, item['idkey'], item['carro']['data']['modelo']])

    # pega item especifico dentro do vetor master
    print("")
    #print(vetor_master)
    #print(len(vetor_master))

    # se tiver mais de 2 carros, efetua o calculo DE entre o primeiro e o segundo da lista.
    if len(vetor_master) > 1:
        # testa a funcao:
        # espera resultado DE como zero.
        v1 =  [5, 5, 5]
        v2 = [[5, 5, 5]]
        de_potencia = gtsCalculos.distancia_euclidiana(v1, v2)
        # mostra os dados processado
        print("v1 = "+ str(v1))
        print("v2 = "+ str(v2[0]))
        print("DE = "+ str(de_potencia))
        print("")

        # calculo para a petencia e torque.
        v1 =  vetor_master[0][0]
        v2 = [vetor_master[1][0]]
        de_potencia = gtsCalculos.distancia_euclidiana(v1, v2)
        # mostra os dados processado
        print("v1 = "+ str(vetor_master[0][0])+"   => "+ str(vetor_master[0][2])+" => "+ str(vetor_master[0][3]))
        print("v2 = "+ str(vetor_master[1][0])+"   => "+ str(vetor_master[1][2])+" => "+ str(vetor_master[1][3]))
        print("DE P "+ str(de_potencia))
        print("")

        # calculo para o desempenho.
        v1 =  vetor_master[0][1]
        v2 = [vetor_master[1][1]]
        de_desempenho = gtsCalculos.distancia_euclidiana(v1, v2)
        # mostra os dados processado.
        print("v1 = "+ str(vetor_master[0][1])+" => "+ str(vetor_master[0][2])+" => "+ str(vetor_master[0][3]))
        print("v2 = "+ str(vetor_master[1][1])+" => "+ str(vetor_master[1][2])+" => "+ str(vetor_master[1][3]))
        print("DE D "+ str(de_desempenho))
        print("")
