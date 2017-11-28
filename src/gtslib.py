# -*- coding: utf-8 -*-
# Neviim - 2017
# V-0.1.0
import json

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


if __name__ == '__main__':
    # usando a classe sobre dados do carro.
    statusCarro = StatusCarro()
    dados = statusCarro.ler_dados_unico('dados_carro')

    print(dados)
