import pandas as pd

df = pd.DataFrame({
    'First Name': ['John', "Ken", "Amy", "Judy", "Anton"],
    'Last Name': ['Mark', "Leens", "Cowly", "Ark", "Woods"],
    'Age': [17, 21, 36, 19, 42],
    'Phone Number': [
        "7423-456-7890",
        "78765473210",
        "75566677671",
        "75566677424",
        "79876543232"
    ]
})

df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.lower()

print(df.head()) 