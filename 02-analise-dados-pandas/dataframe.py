import pandas as pd 

# Criando dados
dados = {
# Cria a coluna nome:    
    "Nome": ["Hugo", "Ana", "Carlos"],
# Cria a coluna idade:        
    "Idade": [17, 20, 25],
# Cria a coluna nota:        
    "Nota": [8.5, 9.0, 7.5]
}

# Cria a tabela no Pandas.
df = pd.DataFrame(dados)

#Mostra a tabela.
print(df)