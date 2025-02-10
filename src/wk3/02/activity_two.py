import pandas as pd 

df = pd.read_csv("./datasets/sdg_index_2000-2022_cp.csv")

print(f"duplicates: {df.duplicated().sum()}")
df.drop_duplicates(inplace=True)

df2 = pd.read_csv("./datasets/sdg_report_2023(in).csv")

df3 = pd.merge(df, df2, on=["country_code", "country"], )
df3.to_csv("./datasets/out.csv", index=False)

print(df3.head())