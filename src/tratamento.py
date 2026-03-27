import os
import pandas as pd
import reverse_geocode as rg

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


def filtrar_amazonia(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()

    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")

    df_amazonia = df[
        (df["lat"] >= -20) & (df["lat"] <= 5) &
        (df["lon"] >= -80) & (df["lon"] <= -45)
    ]

    return df_amazonia


def adicionar_localizacao(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona informações de cidade, estado e país usando reverse_geocode
    """
    if df.empty:
        return df

    df = df.copy()
    
    print("\n🌍 Adicionando informações de localização...")
    
    # Criar lista de coordenadas
    coordenadas = [(row['lat'], row['lon']) for _, row in df.iterrows()]
    
    # Processar em lotes se for muito grande
    print(f"Processando {len(coordenadas)} coordenadas...")
    
    # Usar reverse_geocode para obter localização
    try:
        resultados = rg.search(coordenadas)
        
        # Adicionar colunas ao DataFrame
        df['cidade'] = [r.get('city', '') for r in resultados]
        df['estado'] = [r.get('state', '') for r in resultados]
        df['pais'] = [r.get('country', '') for r in resultados]
        
        print("✅ Localizações adicionadas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao processar localizações: {e}")
        df['cidade'] = ''
        df['estado'] = ''
        df['pais'] = ''
    
    return df


def filtrar_brasil(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra apenas os focos de calor que estão no Brasil
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Verificar se já tem a coluna de país
    if 'pais' not in df.columns:
        print("⚠️ Coluna 'pais' não encontrada. Adicionando localizações primeiro...")
        df = adicionar_localizacao(df)
    
    # Filtrar apenas Brasil (considerando possíveis variações no nome)
    df_brasil = df[df['pais'].str.contains('Brazil|Brasil', case=False, na=False)]
    
    print(f"\n🇧🇷 Focos no Brasil: {len(df_brasil)} de {len(df)} total")
    
    return df_brasil


def resumo_queimadas(df: pd.DataFrame) -> None:
    total = len(df)

    print("\n🔥 RESUMO DAS QUEIMADAS NA AMAZÔNIA")
    print(f"Total de focos detectados: {total}")

    if total > 1000:
        print("⚠️ ALERTA: Alto número de focos de queimadas.")
    elif total > 500:
        print("⚠️ Atenção: nível moderado de focos.")
    else:
        print("✅ Situação sob controle.")


def resumo_por_estado(df: pd.DataFrame) -> None:
    """
    Mostra resumo dos focos por estado brasileiro
    """
    if df.empty:
        return
    
    print("\n📊 RESUMO POR ESTADO (BRASIL)")
    
    # Verificar se tem a coluna de estado
    if 'estado' in df.columns:
        resumo_estados = df['estado'].value_counts()
        
        for estado, qtd in resumo_estados.items():
            if estado and estado != '':  # Ignorar vazios
                print(f"  {estado}: {qtd} focos")
        
        if len(resumo_estados) > 0:
            print(f"\nTotal de estados com focos: {len(resumo_estados)}")
        else:
            print("  Nenhum estado identificado")
    else:
        print("⚠️ Coluna 'estado' não disponível")


def salvar_dados_tratados(df: pd.DataFrame, nome_arquivo: str, pasta_saida: str = "data/tratado") -> str:
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_saida = os.path.join(pasta_saida, nome_arquivo)
    df.to_csv(caminho_saida, index=False, encoding="utf-8")

    print(f"Arquivo tratado salvo em: {caminho_saida}")
    return caminho_saida