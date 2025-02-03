import pandas as pd 

df = pd.DataFrame({
    'name': ['john', 'anna', 'peter', 'linda'],
    'age': [28, 24, 35, 40],
    'city': ['new york', 'paris', 'london', 'berlin']
})

print(df.age)

df['country'] = ['usa', 'france', 'uk', 'germany']
print(df.country)


df.rename(columns={'name': 'Full Name', 'age': 'Years', 'city': 'City Name', 'country': 'Nation'}, inplace=True)

df = df.sort_values(by=['Nation'])
print(df.groupby('Nation')['Years'].mean())
