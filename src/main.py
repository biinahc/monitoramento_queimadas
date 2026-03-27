from coleta import carregar_dados_csv
from tratamento import resumo_inicial
from visualizacao import gerar_grafico_exemplo


def main():
    caminho_arquivo = "data/bruto/dados_queimadas.csv"

    df = carregar_dados_csv(caminho_arquivo)

    if df.empty:
        print("Nenhum dado carregado.")
        return

    resumo_inicial(df)

    # Troque pela coluna real quando soubermos os nomes do arquivo
    # gerar_grafico_exemplo(df, "estado")


if __name__ == "__main__":
    main()