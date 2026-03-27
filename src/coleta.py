import pandas as pd


def carregar_dados_csv(caminho_arquivo: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(caminho_arquivo, sep=",", encoding="utf-8")
        return df
    except Exception as e:
        print(f"Erro ao carregar arquivo CSV: {e}")
        return pd.DataFrame()