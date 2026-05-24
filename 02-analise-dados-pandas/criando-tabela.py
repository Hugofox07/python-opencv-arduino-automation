import pandas as pd 

# Criando dados
dados = {
    "Nomes": ["Hugo", "Ana", "Carlos", "Andreia", " Belinha"],
    "Cidade": ["Campinas", "Belo Horizonte", "Para", "Itatinga", "Maria Rosa"],
    "Profissão": ["Cozinheiro", "Baba", "Limpeza", "Waiters","Robotico"] 
}

df = pd.DataFrame(dados)
print(df)