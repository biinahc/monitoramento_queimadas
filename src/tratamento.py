import os
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


def resumo_queimadas(df: pd.DataFrame) -> None:
    total = len(df)

    print("\n🔥 RESUMO DAS QUEIMADAS")
    print(f"Total de focos detectados: {total}")

    if total > 1000:
        print("⚠️ ALERTA: Alto número de focos de queimadas.")
    elif total > 500:
        print("⚠️ Atenção: nível moderado de focos.")
    else:
        print("✅ Situação sob controle.")


def salvar_dados_tratados(df: pd.DataFrame, nome_arquivo: str, pasta_saida: str = "data/tratado") -> str:
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_saida = os.path.join(pasta_saida, nome_arquivo)
    df.to_csv(caminho_saida, index=False, encoding="utf-8")

    print(f"Arquivo tratado salvo em: {caminho_saida}")
    return caminho_saida