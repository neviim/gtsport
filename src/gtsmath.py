# -*- coding: utf-8 -*-
# Neviim - 2017
# V-0.1.5

__version__ = 'v-0.1.5'

import numpy as np

class GtsCalculos(object):
    """docstring for GtsCalculos."""
    def __init__(self, idkey=0):
        super(GtsCalculos, self).__init__()
        self.idkey = idkey

    def distancia_euclidiana(self, v1, v2):
        """ calcula a distancia eucllidiana entre dois conjuntos de array
                - Parametro:
                    array1 = vetor de dados a ser comparado com array2.
                    array2 = vetor de dados usado para base de GtsCalculos.

                - Uso:
                    v1 =  [1.2, 2.3, 4.5]

                    v2 = [[0.5, 0.7, 0.2],
                          [0.7, 0.2, 2.2],
                          [1.5, 4.7, 0.1]]

                    gtsCalculos = GtsCalculos()
                    dist_euclidiana = gtsCalculos.distancia_euclidiana(v1, v2)

                - Retorno:
                    uma lista com as distancias euclidianas entre o conjuntos de
                    dados de entrada da lista no vetor2 (v2).
        """
        # converte a lista em um array
        xi = np.array(v1)
        resultado = []

        for item in v2:
            yi = np.array(item)
            # dubtrai as arrays
            dif = xi - yi
            # eveva ao quadrado para remover o sinal negativo.
            quad_dist = np.dot(dif, dif)
            dist_eucl = np.sqrt(quad_dist)
            # adiciona a uma lista o resultado da operacao.
            resultado.append(dist_eucl)

        return resultado


if __name__ == '__main__':
    #
    gtsCalculos = GtsCalculos()

    # Parametro da entrada v1
    v1 =  [3.7, 4.8, 2.3]
    # Comparados com parametros das entradas v2
    v2 = [[3.7, 6.2, 4.7],
          [2.7, 3.3, 0.2],
          [3.7, 5.2, 1.4],
          [4.6, 2.4, 3.4]
         ]

    resultado = gtsCalculos.distancia_euclidiana(v1, v2)

    print(" ")
    print("# ------------- ")
    print("Virsão: "+__version__+"\n")
    print("Resultado:")
    print(" ")
    print(resultado)
    print(" ")
    print("Saida:")
    print(" ")
    print("Entrada v1 .....: "+  str(v1))
    print("Escolha v2 .....: "+  str(v2[resultado.index(np.min(resultado))]))
    print("Dist. Euclidiana:  "+ str(np.min(resultado)))
    print("# ------------------------------- ")
    # resultado esperado 4.47
