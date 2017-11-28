# -*- coding: utf-8 -*-
# Neviim - 2017
# V-0.1.0

import numpy as np

class GtsCalculos(object):
    """docstring for GtsCalculos."""
    def __init__(self, idkey=0):
        super(GtsCalculos, self).__init__()
        self.idkey = idkey

    def distancia_euclidiana(self, v1, v2):
        """ calcula a distancia eucllidiana entre dois conjuntos de array
                - Parametro:
                    array1 = vetor de dados a ser comparado com array2
                    array2 = vetor de dados usado para base de GtsCalculos

                - Uso:
                    v1 = [1.2, 2.3, 4.5]
                    v2 = [0.5, 0.7, 0.2]

                    gtsCalculos = GtsCalculos()
                    dist_euclidiana = gtsCalculos.distancia_euclidiana(v1, v2)

                - Retorno:
                    a distancia euclidiana entre estes dois conjuntos de dados.
        """
        # converte a lista em um array
        xi = np.array(v1)
        yi = np.array(v2)
        # dubtrai as arrays
        dif = xi - yi
        # eveva ao quadrado para remover o sinal negativo.
        quad_dist = np.dot(dif, dif)
        dist_eucl = np.sqrt(quad_dist)
        return dist_eucl


if __name__ == '__main__':
    #
    gtsCalculos = GtsCalculos()

    v1 = [5, 7, 9]
    v2 = [5, 5, 5]

    print(gtsCalculos.distancia_euclidiana(v1, v2))
    # resultado esperado 4.47
