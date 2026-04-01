import os
import pandas as pd
import folium
from folium.plugins import HeatMap
from typing import Optional


def gerar_mapa_focos(df: pd.DataFrame, pasta_saida: str = "output/graficos") -> Optional[str]:
    if df.empty or 'lat' not in df.columns or 'lon' not in df.columns:
        print("Dados insuficientes para gerar o mapa de calor.")
        return None

    os.makedirs(pasta_saida, exist_ok=True)
    

    mapa = folium.Map(location=[-15.7801, -47.9292], zoom_start=4, tiles='CartoDB dark_matter')
    

    heat_data = [[row['lat'], row['lon']] for index, row in df.iterrows()]
    
    HeatMap(heat_data, radius=12, blur=15, gradient={0.4: 'yellow', 0.65: 'orange', 1: 'red'}).add_to(mapa)
    
    caminho_mapa = os.path.join(pasta_saida, "mapa_calor_queimadas.html")
    mapa.save(caminho_mapa)
    
    print(f" Mapa de calor interativo salvo em: {caminho_mapa}")
    return caminho_mapa