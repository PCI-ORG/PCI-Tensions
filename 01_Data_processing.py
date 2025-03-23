import pandas as pd

df_taiwan = pd.read_csv("../Data/Raw/[[input.csv]]")
df_taiwan['date'] = pd.to_datetime(df_taiwan.published.astype(str), format='%Y%m%d')
df_taiwan['year_month'] = df_taiwan['date'].dt.to_period('M')
df_taiwan["id"] = ["ID" + str(i).rjust(3, "0") for i in range(len(df_taiwan))]

df_96 = df_taiwan.query("date >= '1994-01-01' and date <= '1996-12-31'")
df_96.sort_values('date', inplace=True)
df_96.to_csv("../Data/Processed/text_96.csv", index=False)

df_24 = df_taiwan.query("date >= '2022-01-01' and date <= '2024-12-31'")
df_24 = df_24.drop(columns='url').drop_duplicates(keep='last')
df_24.to_csv("../Data/Processed/text_24.csv", index=False)
