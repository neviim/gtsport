#!/usr/bin/env python3
# -*-coding: utf-8-*-
# Neviim - 2017
#
from pymongo import MongoClient
import pymongo
import datetime
import hashlib
import shutil
import json
import time
import os


class MonitoraPasta(object):
    """docstring para MonitoraPasta.
        Parametros:
            drOrigem  = Diretorio de origem.
            drDestino = Diretorio destino onde sera movido o aquivo.

            - Caso não seja informado sera adota ../data/dr<1/2> por padrão.

            Uso:
                monitoraPasta = MonitoraPasta(drOrigem, drDestino)
    """
    def __init__(self, drOrigem="../data/dr1", drDestino="../data/dr2"):
        super(MonitoraPasta, self).__init__()
        self.drOrigem  = drOrigem
        self.drDestino = drDestino
        self.tempo = 1
        self.nome = "output_"
        self.extensao = ".txt"
        # funcao lambda idn
        self.novoNome = lambda idn: self.drDestino+"/"+self.nome+str(idn)+self.extensao

        # instancia a classe GranTurismoSport, permite gravar em mongoDB.
        self.gtSport = GranTurismoSport()

    def le_json(self, arquivo):
        """ le um arquivo json e arquiva em uma collection carros
                    Uso:
                        gtSport = GranTurismoSport()
                        arquivoJsonLido = gtSport.le_json(path, arquivo)

                    Retorna:
                        O arquivo json que foi lido.
        """
        arquivo_aberto = open(self.drOrigem +'/'+ arquivo)
        jsonCarro = json.load(arquivo_aberto)
        return jsonCarro

    def tem_arquivo(self):
        """ havendo arquivo na pasta Origem, ele sera processado.
                Uso:
                    monitoraPasta.tem_arquivo()
        """
        listArquivos = os.listdir(self.drOrigem)

        # caso haja arquivo no diretorio origem.
        if len(listArquivos) > 0:
            for arquivo in listArquivos:
                arquivoOriguem = self.drOrigem+"/"+arquivo

                # Cadastra status de carro do Gran Turismo Sport
                # em DataBase coletania MongoDB.
                if arquivo == "gtsCarro.json": # este é um nome especifico.
                    self.gtSport.cadastra_carro(self.le_json(arquivo))
                # ----------------------------------------------------

                # remomeia o arquivo, idn não sera repetido.
                idn = 1; arquivoRenomeado = self.novoNome(idn)
                while os.path.exists(arquivoRenomeado):
                    idn = idn+1; arquivoRenomeado = self.novoNome(idn)

                # o arquivo é novido ao drDestino.
                shutil.move(arquivoOriguem, arquivoRenomeado)
                print("Aquivo: "+arquivo+" processado.")
        return


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


# inicio da aplicação.
if __name__ == "__main__":
    # path dos diretorios origem e destino
    dr1 = "../data/dr1" # origem
    dr2 = "../data/dr2" # destino
    tempo = 10 # tempo de espera em segundos

    # ativa classe de monitoramento de pasta.
    monitorandoPasta = MonitoraPasta(dr1, dr2)

    # loop infinito.
    print("Monitoramento inicializado, (CTRL+C) para cancelar.")

    while True:
        monitorandoPasta.tem_arquivo()
        time.sleep(tempo)
