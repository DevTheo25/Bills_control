import pandas as pd
import sqlite3




# Conectar ao banco de dados
connection = sqlite3.connect('finanças.db')
cursor = connection.cursor()

# query = "DELETE FROM tasks"
# cursor.execute(query)
# connection.commit()

# # Ler os dados atualizados
query = "SELECT * FROM tasks"
df = pd.read_sql_query(query, connection)




# Fechar a conexão
connection.close()

# Exibir os dados
print(df)
