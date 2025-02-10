import pandas as pd 


def process(dataframe):
    print("processing dataset")
    print(f"  found {dataframe.duplicated().sum()} duplicates")
    print(f"  found {dataframe.isnull().sum().sum()} null values")
    dataframe.drop_duplicates(inplace=True)    
    dataframe.dropna(inplace=True)
    return dataframe

df = process(pd.read_csv("./datasets/sdg_index_2000-2022_cp.csv"))
df2 = process(pd.read_csv("./datasets/sdg_report_2023(in).csv"))

df3 = process(pd.merge(df, df2, on=["country_code", "country"]))
df3.to_csv("./datasets/out.csv", index=False)

print(df3.head())