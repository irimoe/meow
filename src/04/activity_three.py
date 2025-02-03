import pandas as pd

df = pd.read_csv('./datasets/data.csv')

print(f"found {df.isnull().sum().sum()} missing values")

df.fillna(df.mean(), inplace=True)
print("\ndata after filling missing values:\n", df)

mean_duration = df['Duration'].mean()
for i in range(len(df)): 
   if df.loc[i, 'Duration'] > 300: df.loc[i, 'Duration'] = mean_duration

print("\ndata after fixing outliers in `duration` column:\n", df)
print(f"found {df.duplicated().sum()} duplicate values")

df.drop_duplicates(inplace=True)
print("\ndata after removing duplicate values:\n", df)