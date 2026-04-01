import os
import pandas as pd
import reverse_geocoder as rg


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

    print("\n RESUMO DAS QUEIMADAS")
    print(f"Total de focos detectados: {total}")

    if total > 1000:
        print(" ALERTA: Alto número de focos de queimadas.")
    elif total > 500:
        print(" Atenção: nível moderado de focos.")
    else:
        print(" Situação sob controle.")


def salvar_dados_tratados(df: pd.DataFrame, nome_arquivo: str, pasta_saida: str = "data/tratado") -> str:
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_saida = os.path.join(pasta_saida, nome_arquivo)
    df.to_csv(caminho_saida, index=False, encoding="utf-8")

    print(f"Arquivo tratado salvo em: {caminho_saida}")
    return caminho_saida


def adicionar_cidade_estado(df: pd.DataFrame) -> pd.DataFrame:
    """Busca a cidade e estado baseados nas coordenadas lat/lon de forma ultra rápida (offline)."""
    if df.empty or 'lat' not in df.columns or 'lon' not in df.columns:
        print("Coordenadas (lat/lon) não encontradas para geocodificação.")
        return df

    print("\n🌍 Buscando cidades e estados baseados nas coordenadas (Modo Turbo/Offline)...")
    
    coords = []
    for index, row in df.iterrows():
        try:
            lat = float(str(row['lat']).replace(',', '.'))
            lon = float(str(row['lon']).replace(',', '.'))
            coords.append((lat, lon))
        except:
            coords.append((0.0, 0.0))
    
    try:
        resultados = rg.search(tuple(coords), mode=1)
        
        cidades = []
        estados = []
        
        for res, original_coord in zip(resultados, coords):
            if original_coord == (0.0, 0.0):
                cidades.append("Invalido")
                estados.append("Invalido")
            else:
                cidades.append(res.get('name', 'Desconhecido'))
                estados.append(res.get('admin1', 'Desconhecido'))
    except Exception as e:
        print(f"Erro na conversao de coordenadas: {e}")
        cidades = ["Erro"] * len(df)
        estados = ["Erro"] * len(df)

    df_copy = df.copy()
    df_copy['cidade'] = cidades
    df_copy['estado'] = estados

    print(f"✅ {len(df)} pontos processados rapidamente!")
    return df_copy


def salvar_dados_excel(df: pd.DataFrame, nome_arquivo: str, pasta_saida: str = "output/dados") -> str:
    """Exporta o dataframe final contendo as novas colunas para o Excel (.xlsx)."""
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_saida = os.path.join(pasta_saida, nome_arquivo)
    df.to_excel(caminho_saida, index=False)

    print(f"📊 Relatório em Excel salvo em: {caminho_saida}")
    return caminho_saida