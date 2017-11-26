# gtsport

Gran turismo sport

  Le todo arquivo json colocado em uma pasta especifica e o cadastra em um banco mongodb previamente configurado.

  Mongodb:
    DataBase   => GranTurismoSport
    Collection => carros

  - Ao ler e reconhecer o arquivo pelo nome especifico (gtsCarro.json), automaticamente o arquivo será identificado, uma copia do mesmo será feita no diretório ../data/dr2 e o conteúdo do arquivo será processado, gerando um item collection no banco. o arquivo original será deletado do diretório ../data/dr1

  - A estrutura do diretório de gtSport precisa estar desta forma.

    ..
    data
      dr1
      dr2
    src


Dependência:

    $ pip3 install pymongo
