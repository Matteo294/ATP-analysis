import plotly.express as px
import pandas as pd
import sqlite3
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

import plotly.express as px
import sqlite3
import pandas as pd

years = [2020, 2021, 2022, 2023, 2024]
players = ["sinner", "alcaraz", "djokovic", "zverev", "fritz", "medvedev"]

# Connessione al database
conn = sqlite3.connect("D:\\code\\GitHub\\ATP-analysis\\data.db")
cur = conn.cursor()


#   WINRATE
##################################################################################################
# Creazione del dataframe per Plotly
data = []

for name in players:
    wr = []
    for y in years:
        # Conta le vittorie
        cur.execute(f"SELECT COUNT(*) FROM {name} WHERE win='yes' and tourney_date LIKE '{y}%'")
        w = cur.fetchone()[0]

        # Conta le sconfitte
        cur.execute(f"SELECT COUNT(*) FROM {name} WHERE win='no' and tourney_date LIKE '{y}%'")
        l = cur.fetchone()[0]

        # Calcola il win rate
        if (w + l) > 0:
            win_rate = w / (w + l) * 100
        else:
            win_rate = None  # Evita divisione per zero

        data.append({"Year": int(y), "Player": name.title(), "WinRate": win_rate})

# Converti in DataFrame
df = pd.DataFrame(data)

# Crea il grafico interattivo con Plotly
fig = px.line(df, x="Year", y="WinRate", color="Player",
              markers=True, title="Win Rate per Anno",
              labels={"WinRate": "Win Rate (%)", "Year": "Anno"},
              line_shape="linear")

fig.update_layout(yaxis=dict(tickvals=[40, 60, 80, 100], ticktext=["40%", "60%", "80%", "100%"]))
fig.update_layout(xaxis=dict(tickvals=years, ticktext=[str(y) for y in years]))
fig.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
fig.update_traces(line=dict(width=2))

# Salva il grafico come file HTML
fig.write_html("D:\\code\\GitHub\\ATP-analysis\\plots\\winrate_per_year.html")
print("Grafico salvato come winrate_per_year.html")
##################################################################################################





#   FIRST SERVE PERCENTAGE 
##################################################################################################
years = [2020, 2021, 2022, 2023, 2024]
players = ["sinner", "alcaraz", "djokovic", "zverev", "fritz", "medvedev"]

# Crea figura con 2x2 subplot
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Ace %", "First In %", "Double Fault %", "First Won %"),
    horizontal_spacing=0.12,
    vertical_spacing=0.15
)

# Per ogni giocatore, calcola i valori per ogni metrica
for name in players:
    ace_values, fin_values, df_values, fwon_values, ace_dev, fin_dev, df_dev, fwon_dev = [[] for _ in range(8)]

    for y in years:
        cmd = f"SELECT firstIn, df, firstWon, ace, serve_points FROM {name} WHERE tourney_date LIKE '{y}%';"
        cur.execute(cmd)
        results = cur.fetchall()

        # Separa i dati
        firstIn = [r[0] for r in results]
        df = [r[1] for r in results]
        firstWon = [r[2] for r in results]
        ace = [r[3] for r in results]
        serve_points = [r[4] for r in results]

        def compute_ratio(val, sp):
            return [100 * v1 / v2 for v1, v2 in zip(val, sp) if v1 is not None and v2 not in (None, 0)]

        ace_values.append(np.average(compute_ratio(ace, serve_points)) if compute_ratio(ace, serve_points) else None)
        fin_values.append(np.average(compute_ratio(firstIn, serve_points)) if compute_ratio(firstIn, serve_points) else None)
        df_values.append(np.average(compute_ratio(df, serve_points)) if compute_ratio(df, serve_points) else None)
        fwon_values.append(np.average(compute_ratio(firstWon, serve_points)) if compute_ratio(firstWon, serve_points) else None)
        ace_dev.append(np.std(compute_ratio(ace, serve_points)) / np.average(compute_ratio(ace, serve_points)) 
                       if compute_ratio(ace, serve_points) else None)
        fin_dev.append(np.std(compute_ratio(firstIn, serve_points)) / np.average(compute_ratio(firstIn, serve_points))
                        if compute_ratio(firstIn, serve_points) else None)
        df_dev.append(np.std(compute_ratio(df, serve_points)) / np.average(compute_ratio(df, serve_points))
                      if compute_ratio(df, serve_points) else None)
        fwon_dev.append(np.std(compute_ratio(firstWon, serve_points)) / np.average(compute_ratio(firstWon, serve_points)) 
                        if compute_ratio(firstWon, serve_points) else None)


    # Aggiungi ogni traccia alla rispettiva subplot
    fig.add_trace(go.Scatter(x=years, y=ace_values, mode='lines+markers', name=name.title(), 
                             error_y=dict(type='data', array=ace_dev, visible=True)), row=1, col=1)
    fig.add_trace(go.Scatter(x=years, y=fin_values, mode='lines+markers', name=name.title(), showlegend=False, 
                             error_y=dict(type='data', array=fin_dev, visible=True)), row=1, col=2)
    fig.add_trace(go.Scatter(x=years, y=df_values, mode='lines+markers', name=name.title(), showlegend=False, 
                             error_y=dict(type='data', array=df_dev, visible=True)), row=2, col=1)
    fig.add_trace(go.Scatter(x=years, y=fwon_values, mode='lines+markers', name=name.title(), showlegend=False, 
                             error_y=dict(type='data', array=fwon_dev, visible=True)), row=2, col=2)

# Aggiorna layout
fig.update_layout(
    title_text="Serve Stats per Player (per Year)",
    height=700,
    width=950,
    legend_title="Players",
    plot_bgcolor='white',
    margin=dict(t=60, b=40, l=40, r=40)
)

# Aggiusta assi (opzionale, puoi rimuovere per default)
fig.update_yaxes(title_text="%", row=1, col=1, range=[1, 16])
fig.update_yaxes(title_text="%", row=1, col=2, range=[57, 76])
fig.update_yaxes(title_text="%", row=2, col=1, range=[1, 7])
fig.update_yaxes(title_text="%", row=2, col=2, range=[42, 58])

# Salva in HTML
fig.write_html("D:\\code\\GitHub\\ATP-analysis\\plots\\serve_stats.html")
print("Grafico salvato come serve_stats.html")
##################################################################################################

conn.close()