import os
from pathlib import Path
from coleta import carregar_dados_csv
from tratamento import (
    resumo_inicial,
    resumo_queimadas,
    salvar_dados_tratados,
    adicionar_cidade_estado,
    salvar_dados_excel
)
from visualizacao import gerar_mapa_focos

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

        df = adicionar_cidade_estado(df)
        resumo_queimadas(df)

        nome_saida = f"tratado_{arquivo.name}"
        salvar_dados_tratados(df, nome_saida)
        
        nome_excel = arquivo.name.replace(".csv", ".xlsx")
        salvar_dados_excel(df, nome_excel)

        print("\nGerando mapa interativo...")
        gerar_mapa_focos(df)

        print("\nProcessamento concluído com sucesso.")

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()