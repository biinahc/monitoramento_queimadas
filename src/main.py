import os
from pathlib import Path
from coleta import carregar_dados_csv
from tratamento import (
    resumo_inicial,
    filtrar_amazonia,
    resumo_queimadas,
    salvar_dados_tratados
)
from visualizacao import gerar_grafico_por_satelite

PASTA_DADOS = Path("data/bruto")


def obter_arquivo_mais_recente(pasta: Path) -> Path:
    arquivos = list(pasta.glob("*.csv"))

    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo CSV encontrado na pasta.")

    return max(arquivos, key=os.path.getctime)


def main():
    try:
        print("Buscando arquivo mais recente...")

        arquivo = obter_arquivo_mais_recente(PASTA_DADOS)
        print(f"Arquivo encontrado: {arquivo}")

        print("\nCarregando dados...")
        df = carregar_dados_csv(str(arquivo))

        if df.empty:
            print("Erro ao carregar dados.")
            return

        resumo_inicial(df)

        print("\nFiltrando focos na região da Amazônia...")
        df_amazonia = filtrar_amazonia(df)

        resumo_queimadas(df_amazonia)

        nome_saida = f"amazonia_{arquivo.name}"
        salvar_dados_tratados(df_amazonia, nome_saida)

        print("\nGerando gráfico...")
        gerar_grafico_por_satelite(df_amazonia)

        print("\nProcessamento concluído com sucesso.")

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()