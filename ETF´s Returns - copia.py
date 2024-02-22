# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 19:38:27 2024

@author: rubof
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.modules import custom_functions as cf 

etf = cf.data_dict(R"C:\Users\rubof\Desktop\KaxaNuk\Retornos ETF´s\Data")

def annual_return(etf_dict):
    annual_returns = pd.DataFrame()

    for etf_name, df in etf_dict.items():
        df["m_date"] = pd.to_datetime(df["m_date"])
        annual_log_returns = df.groupby(df['m_date'].dt.year)["c_log_returns_adjusted_close"].sum().reset_index()
        annual_log_returns.rename(columns={"c_log_returns_adjusted_close": etf_name}, inplace=True)
        annual_log_returns.set_index("m_date", inplace=True)
        annual_returns = annual_returns.join(annual_log_returns, how="outer")

    return annual_returns

log_returns = annual_return(etf)
normal_returns = np.exp(log_returns)-1
returns_graph = normal_returns .loc[2011:].transpose()

ranked_returns = returns_graph.rank(axis=0, ascending=True) - 1
# Ahora, usamos 'ranked_returns' para ordenar 'returns_graph' de manera descendente
sorted_returns = pd.DataFrame(index=returns_graph.index, columns=returns_graph.columns)
for year in returns_graph.columns:
    sorted_returns[year] = returns_graph[year].iloc[ranked_returns[year].argsort()]

# Asignamos un color único a cada ETF.
custom_colors = ["#e84328", "#F09A8C", "#aaaaff", "#8cd0d3", 
                 "#00b060", "#00aaff", "#AA7100", "#C7C7C7", 
                 "#ffaa00", "#FFD480"]
colors = custom_colors[:len(returns_graph.index)]

# Creamos la figura y los ejes.
fig, ax = plt.subplots(figsize=(15, 6))

# Creamos un gráfico de flujo para cada ETF.
for idx, etf in enumerate(sorted_returns.index):
    y_values = sorted_returns.loc[etf]
    # Dibujamos los bloques de flujo para el ETF.
    for year_idx, year in enumerate(sorted_returns.columns):
        value = y_values[year]
        position = ranked_returns.loc[etf, year]
        ax.add_patch(
            plt.Rectangle(
                (year_idx, position), 1, 0.969,
                facecolor=colors[idx], edgecolor="white"
            )
        )
        # Añadimos el texto del rendimiento y el nombre del ETF dentro del bloque.
        ax.text(year_idx + 0.5, position + 0.5, f"{etf}\n{value:.2%}",
                ha='center', va='center', color='black', fontsize=9)

# Configuramos los límites y las etiquetas de los ejes.
ax.set_xticks(np.arange(len(sorted_returns.columns)) + 0.5)
ax.set_xticklabels(sorted_returns.columns)
ax.set_yticks(np.arange(len(sorted_returns.index)) + 0.5)
# Ocultamos las etiquetas del eje Y.
ax.set_yticklabels([])
# Ajustamos los límites de los ejes.
ax.set_xlim(0,  len(sorted_returns.columns))
ax.set_ylim(0, len(sorted_returns.index))

# Añadimos el título.
ax.set_title("ETF performance")

plt.show()
