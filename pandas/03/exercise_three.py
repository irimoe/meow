import pandas as pd

df = pd.read_csv('./datasets/iris.csv')

print(df.head(15))
print(df.tail(15))
print()

print(df.describe())
print()

print(df.isnull().sum())
print()

df2 = df.fillna(0)
df.fillna(0, inplace=True)

print(df2.head())