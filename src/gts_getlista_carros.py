# -*- coding: UTF-8 -*-
#
# Por: Neviim Jads - 2017

import json 
import pandas as pd 

from urllib.request import urlopen
from bs4 import BeautifulSoup


class GtsCarros(object):
	""" Classe GtsCarros, faz um scraping de todos os carros disponiveis no GTS atualmente.
	
		Arguments:
			object {[type]} -- [description]
	"""
	def __init__(self):
		""" Inicialização das variaveis da classes"""
		super(GtsCarros, self).__init__()
		url  = "https://www.gran-turismo.com/br/products/gtsport/carlist/"
		html = urlopen(url)
		soup = BeautifulSoup(html, 'lxml')
		self.table = soup.find('div', class_='carlist_table')

	def ler_tabelas(self):
		""" Le a tabela de uma pagina htmp que contem a lista 
			de carros do Gran Turismo Sport
		"""
		A=[] # marca
		B=[] # carro
		C=[] # categoria
		
		for row in self.table.findAll("dl"):
			cells = row.findAll('dd')
			
			# monta as listas com todas as marcas, carros e categoria
			if len(cells)==3:
				A.append(cells[0].find(text=True))
				B.append(cells[1].find(text=True))
				C.append(cells[2].find(text=True))

		# cria um dataframe com a relação de carros capturada 
		data = {'marca': A, 'carro': B, 'categoria': C}
		df = pd.DataFrame.from_dict(data)

		# gera um arquivo json com os dados
		carros = df.to_json(orient='table')
		return carros # retorna arquivo formato json

	def gravar_json(lista, f_arquivo='gtslistacarros', path='../data'):
		""" gera um f_arquivo json em disco
		
			Arguments:
				lista {[dict]} -- [dicionario contendo a marca, carro e categoria]
			
			Keyword Arguments:
				f_arquivo {str} -- [nome do f_arquivo json a ser gerado] (default: {'gtslistacarros'})
				path {str} -- [path onde sera gerado o f_arquivo json] (default: {'../data'})
		"""
		with open(path+'/'+f_arquivo+'.json', 'w', encoding='utf-8') as farq:
			json.dump(lista, farq)
		return
	
	def ler_json(arquivo='gtslistacarros', path='../data'):
		""" le um determinado arquivo gerado no formato json
		
			Keyword Arguments:
				arquivo {str}   -- [nome do arquivo a ser carregado] (default: {'gtslistacarros'})
				path {str}      -- [path de umde se encontra o arquivo] (default: {'../data'})

			Retorna:
				Um dicionario contendo toda tabela de carros do GTS no formato json.
		"""
		with open(path+'/'+arquivo+'.json', 'r', encoding='utf-8') as farq:
			return json.load(farq)


# - main()
def main():
    gtscarros = GtsCarros()
    carros = gtscarros.ler_tabelas()
    gtscarros.gravar_json(carros)
    return


# -- main --
if __name__ == '__main__':
    main()

