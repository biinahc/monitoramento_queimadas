import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium
from folium.plugins import HeatMap
from typing import Optional


def gerar_grafico_por_satelite(df: pd.DataFrame, pasta_saida: str = "output/graficos") -> Optional[str]:
    if df.empty:
        print("DataFrame vazio. Nenhum gráfico foi gerado.")
        return None

    if "satelite" not in df.columns:
        print("A coluna 'satelite' não existe no DataFrame.")
        return None

    os.makedirs(pasta_saida, exist_ok=True)

    contagem = df["satelite"].value_counts()

    # Aplica um estilo base mais moderno
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except:
        plt.style.use('ggplot')

    # Ajusta o tamanho da figura para melhor proporção
    fig, ax = plt.subplots(figsize=(12, 7))

    # Paleta de cores num gradiente de calor (Fire/Laranja)
    color_map = plt.colormaps['YlOrRd'] if hasattr(plt, 'colormaps') else plt.cm.YlOrRd
    colors = color_map(np.linspace(0.9, 0.4, len(contagem)))

    # Gera as barras com bordas escuras
    bars = ax.bar(contagem.index, contagem.values, color=colors, edgecolor='#660000', linewidth=1.5, alpha=0.85)

    # Titulos e Labels embelezados
    ax.set_title("🔥 Focos de Queimadas por Satélite", fontsize=18, fontweight='bold', pad=20, color='#333333')
    ax.set_xlabel("Nomes dos Satélites", fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel("Quantidade de Focos Detectados", fontsize=12, fontweight='bold', labelpad=10)

    # Limpando bordas e destacando a grid
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Coloca os numeros de forma legível em cima de cada barra
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2., 
            height + (height * 0.01), 
            f'{int(height):,}', 
            ha='center', 
            va='bottom', 
            fontsize=12, 
            fontweight='bold', 
            color='#333333'
        )

    # Rotacionando os nomes dos satelites para nao se embolem
    plt.xticks(rotation=45, ha='right', fontsize=11, fontweight='500')
    plt.yticks(fontsize=11)
    
    plt.tight_layout()

    caminho = os.path.join(pasta_saida, "grafico_focos_por_satelite.png")
    # Salva com alta resolução
    fig.savefig(caminho, dpi=300, bbox_inches='tight')
    plt.close(fig)

    print(f"Gráfico premium salvo em: {caminho}")
    return caminho

def gerar_mapa_focos(df: pd.DataFrame, pasta_saida: str = "output/graficos") -> Optional[str]:
    if df.empty or 'lat' not in df.columns or 'lon' not in df.columns:
        print("Dados insuficientes para gerar o mapa de calor.")
        return None

    os.makedirs(pasta_saida, exist_ok=True)
    
    # Centro aproximado do Brasil
    mapa = folium.Map(location=[-15.7801, -47.9292], zoom_start=4, tiles='CartoDB dark_matter')
    
    # Prepara os dados de calor (Lat, Lon)
    heat_data = [[row['lat'], row['lon']] for index, row in df.iterrows()]
    
    # Adiciona o mapa de calor com gradiente apropriado de fogo
    HeatMap(heat_data, radius=12, blur=15, gradient={0.4: 'yellow', 0.65: 'orange', 1: 'red'}).add_to(mapa)
    
    caminho_mapa = os.path.join(pasta_saida, "mapa_calor_queimadas.html")
    mapa.save(caminho_mapa)
    
    print(f"🌍 Mapa de calor interativo salvo em: {caminho_mapa}")
    return caminho_mapa