import pandas as pd

df = pd.read_csv('pokedex.csv')
print(df.head(5))
df = df.drop(columns=['Ability I', 'Ability II', 'Hidden Ability', 'EV Worth', 'Gender', 'Egg Group I', 'Egg Group II'])
print(df.head(5))