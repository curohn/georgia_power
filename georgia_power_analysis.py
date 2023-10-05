import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import Data
df_2021 = pd.read_csv('GPC_Usage_2021.csv')
df_2022 = pd.read_csv('GPC_Usage_2022.csv')
df_2023 = pd.read_csv('GPC_Usage_2023.csv')
frames = [df_2021, df_2022, df_2023]
df = pd.concat(frames, ignore_index=True)

# Clean and Sort
df[['start_date', 'end_date']] = df['Billing Period'].str.split(' - ', expand=True)
df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date'] = pd.to_datetime(df['end_date'])

# Adding & Modifying Fields
df['time_difference'] = df['end_date'] - df['start_date']
df['days'] = df['time_difference'].dt.total_seconds() / (60 * 60 * 24)
df['cost_per_day'] = df['Cost'] / df['days']
df['avg_temp'] = (df['High Temp'] + df['Low Temp']) / 2
new_column_order = [
    'Billing Period', 'start_date', 'end_date', 'days', 'Cost', 'cost_per_day', 'High Temp', 'Low Temp', 'avg_temp'
]
df = df[new_column_order]
new_column_names = {
    'Billing Period': 'billing_period',
    'start_date': 'start_date',
    'end_date': 'end_date',
    'days': 'days',
    'Cost': 'cost',
    'cost_per_day': 'cost_per_day',
    'High Temp': 'high_temp',
    'Low Temp': 'low_temp',
    'avg_temp': 'avg_temp'
}
df.rename(columns=new_column_names, inplace=True)
df.sort_values(by='start_date', inplace=True)

# Plotting
'''
# Cost over time
plt.plot(df['start_date'], df['cost'],  color='green', marker='o', linestyle='-')
plt.xlabel('Date')
plt.ylabel('Cost')
plt.title('Cost over Time')
plt.xticks(rotation=45)
plt.show()
'''
# Two axis
fig, ax1 = plt.subplots()
color = 'tab:green'
ax1.set_xlabel('Date')
ax1.set_ylabel('Cost')
ax1.plot(df['start_date'], df['cost'], color='green', marker='o', linestyle='-')
ax1.tick_params(axis='y', labelcolor=color)
plt.xticks(rotation=45)
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Avg Temp', color=color)
ax2.plot(df['start_date'], df['avg_temp'], color='blue', marker='o', linestyle='-')
ax2.tick_params(axis='y', labelcolor=color)
plt.show()

