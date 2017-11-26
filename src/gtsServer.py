#!/usr/bin/env python3
# -*-coding: utf-8-*-
# Neviim - 2017
#
from pymongo import MongoClient
import datetime
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
                    # jsonArquivo = self.le_json(arquivo)
                    self.gtSport.cadastra_carro(self.le_json(arquivo))
                # -------------------------------------------

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
        # Colesão de carros
        self.carros = db.carros

    def cadastra_carro(self, carro):
        """ cadastra o os dados pasado por parametro no dicionario carro
                - Parametros:
                    carro => dicionario com os dados do carro a ser cadastrado.

                - Uso:
                    granturismosport = GranTurismoSport()
                    granturismosport.cadastro_carro(<status_carro_json>)

        """
        carro = self.carros.insert_one(carro).inserted_id
        print (carro)


if __name__ == "__main__":
    # path dos diretorios origem e destino
    dr1 = "../data/dr1" # origem
    dr2 = "../data/dr2" # destino
    tempo = 10 # tempo de espera em segundos

    # ativa classe de monitoramento de fasta.
    monitorandoPasta = MonitoraPasta(dr1, dr2)

    # loop infinito.
    print("Monitoramento inicializado, (CTRL+C) para cancelar.")

    while True:
        monitorandoPasta.tem_arquivo()
        time.sleep(tempo)
