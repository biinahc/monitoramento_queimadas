import os
import pandas as pd
import matplotlib.pyplot as plt
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

    plt.figure(figsize=(10, 6))
    contagem.plot(kind="bar")
    plt.title("Focos de Queimadas por Satélite")
    plt.xlabel("Satélite")
    plt.ylabel("Quantidade de Focos")
    plt.xticks(rotation=45)
    plt.tight_layout()

    caminho = os.path.join(pasta_saida, "grafico_focos_por_satelite.png")
    plt.savefig(caminho)
    plt.close()

    print(f"Gráfico salvo em: {caminho}")
    return caminho