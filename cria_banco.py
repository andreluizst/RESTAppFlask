import sqlite3

conexao = sqlite3.connect('banco_0.db')
cursor = conexao.cursor()

cria_tabela = 'create table if not exists hoteis (id next primary key, nome text,\
 estrelas real, diaria real, cidade text)'

cria_hotel = "insert into hoteis values(1, 'Alpha Hotel', 4.3, 345.30, 'Rio de Janeiro')"

cursor.execute(cria_tabela)
cursor.execute(cria_hotel)
conexao.commit()
conexao.close()
