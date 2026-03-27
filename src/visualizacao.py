import os
import pandas as pd
import matplotlib.pyplot as plt


def gerar_grafico_exemplo(df: pd.DataFrame, coluna: str, pasta_saida: str = "output/graficos") -> None:
    if df.empty:
        print("DataFrame vazio. Nenhum gráfico foi gerado.")
        return

    if coluna not in df.columns:
        print(f"A coluna '{coluna}' não existe no DataFrame.")
        return

    os.makedirs(pasta_saida, exist_ok=True)

    contagem = df[coluna].value_counts()

    plt.figure(figsize=(10, 6))
    contagem.plot(kind="bar")
    plt.title(f"Distribuição por {coluna}")
    plt.xlabel(coluna)
    plt.ylabel("Quantidade")
    plt.xticks(rotation=45)
    plt.tight_layout()

    caminho = os.path.join(pasta_saida, f"grafico_{coluna}.png")
    plt.savefig(caminho)
    plt.close()

    print(f"Gráfico salvo em: {caminho}")