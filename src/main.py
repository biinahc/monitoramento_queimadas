import os
from pathlib import Path
from coleta import carregar_dados_csv
from tratamento import (
    resumo_inicial,
    filtrar_amazonia,
    adicionar_localizacao,
    filtrar_brasil,
    resumo_queimadas,
    resumo_por_estado,
    salvar_dados_tratados
)
from visualizacao import gerar_grafico_por_satelite, gerar_grafico_por_estado

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
        
        print(f"Focos na Amazônia: {len(df_amazonia)}")
        
        if df_amazonia.empty:
            print("Nenhum foco encontrado na Amazônia.")
            return
        
        # ADICIONAR LOCALIZAÇÃO (cidade/estado/país)
        print("\n🔍 Adicionando informações de localização...")
        df_amazonia = adicionar_localizacao(df_amazonia)
        
        # FILTRAR APENAS BRASIL
        print("\n🇧🇷 Filtrando apenas focos no Brasil...")
        df_brasil = filtrar_brasil(df_amazonia)
        
        if df_brasil.empty:
            print("Nenhum foco no Brasil encontrado.")
            return
        
        # RESULTADOS
        print("\n" + "="*50)
        print("RESULTADOS FINAIS - FOCOS NO BRASIL")
        print("="*50)
        
        resumo_queimadas(df_brasil)
        resumo_por_estado(df_brasil)
        
        # SALVAR ARQUIVOS
        print("\n💾 Salvando arquivos...")
        
        # Salvar apenas Brasil
        nome_saida_brasil = f"brasil_{arquivo.name}"
        salvar_dados_tratados(df_brasil, nome_saida_brasil)
        
        # Salvar também a Amazônia completa (com todos os países)
        nome_saida_amazonia = f"amazonia_completa_{arquivo.name}"
        salvar_dados_tratados(df_amazonia, nome_saida_amazonia)
        
        # GERAR GRÁFICOS
        print("\n📊 Gerando gráficos...")
        gerar_grafico_por_satelite(df_brasil)
        gerar_grafico_por_estado(df_brasil)
        
        # Mostrar alguns exemplos
        print("\n📌 EXEMPLOS DE FOCOS NO BRASIL:")
        print(df_brasil[['lat', 'lon', 'cidade', 'estado', 'satelite', 'data']].head(10))
        
        # Estatísticas adicionais
        if 'estado' in df_brasil.columns:
            top_estados = df_brasil['estado'].value_counts().head(5)
            print("\n🏆 TOP 5 ESTADOS COM MAIS FOCOS:")
            for estado, qtd in top_estados.items():
                if estado:
                    print(f"  {estado}: {qtd} focos ({qtd/len(df_brasil)*100:.1f}%)")
        
        print("\n✅ Processamento concluído com sucesso!")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()