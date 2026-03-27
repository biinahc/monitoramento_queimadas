import pandas as pd


def resumo_inicial(df: pd.DataFrame) -> None:
    if df.empty:
        print("DataFrame vazio.")
        return

    print("\nPrimeiras linhas:")
    print(df.head())

    print("\nColunas:")
    print(df.columns.tolist())

    print("\nInformações gerais:")
    print(df.info())