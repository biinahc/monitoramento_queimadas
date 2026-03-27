import pandas as pd

def carregar_dados_csv(caminho_arquivo: str) -> pd.DataFrame:
    """
    Carrega dados do CSV e faz tratamento inicial
    """
    try:
        df = pd.read_csv(caminho_arquivo)
        
        # Converter lat/lon para numérico
        df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
        df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
        
        # Remover linhas com coordenadas inválidas
        df = df.dropna(subset=["lat", "lon"])
        
        print(f"Dados carregados: {len(df)} registros")
        return df
        
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return pd.DataFrame()