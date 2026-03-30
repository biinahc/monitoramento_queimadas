import os
from pathlib import Path
from coleta import carregar_dados_csv
from tratamento import (
    resumo_inicial,
    resumo_queimadas,
    salvar_dados_tratados
)
from visualizacao import gerar_grafico_por_satelite, gerar_mapa_focos

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

        resumo_queimadas(df)

        nome_saida = f"tratado_{arquivo.name}"
        salvar_dados_tratados(df, nome_saida)

        print("\nGerando gráficos e mapas...")
        gerar_grafico_por_satelite(df)
        gerar_mapa_focos(df)

        print("\nProcessamento concluído com sucesso.")

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()