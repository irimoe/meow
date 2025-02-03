import pandas as pd 

df = pd.read_json('./datasets/iris.json')
print(df.head())
print(df.count())
print(df.max())
print(df.min())
