#%%
import pandas as pd

df_taiwan = pd.read_csv("Data/Raw/2647d8f4-bf37-492b-b78d-365bb7968382.csv")


df_taiwan['date'] = pd.to_datetime(df_taiwan.published.astype(str), format='%Y%m%d')

df_taiwan

#%%


# 1996 crisis data

df_96 = df_taiwan.query("date >= '1993-01-01' and date <= '1997-12-31'")
df_96.sort_values('date', inplace=True)

# No duplications
assert df_96.drop(columns='url').drop_duplicates().equals(df_96.drop(columns='url'))


df_96['year_month'] = df_96['date'].dt.to_period('M')

df_96["id"] = ["ID" + str(i).rjust(3, "0") for i in range(len(df_96))]

df_96.to_csv("Data/Processed/96_crisis.csv", index=False)

df_96.year_month.value_counts().sort_index().plot()


# %%


# Pelosi visit data

df_pelosi = df_taiwan.query("date >= '2021-01-01' and date <= '2023-12-31'")
df_pelosi.sort_values('date', inplace=True)

# No duplications
assert df_pelosi.drop(columns='url').drop_duplicates().equals(df_pelosi.drop(columns='url'))


df_pelosi['year_month'] = df_pelosi['date'].dt.to_period('M')

df_pelosi["id"] = ["ID" + str(i).rjust(3, "0") for i in range(len(df_pelosi))]

df_pelosi.to_csv("Data/Processed/pelosi.csv", index=False)

df_pelosi.year_month.value_counts().sort_index().plot()


