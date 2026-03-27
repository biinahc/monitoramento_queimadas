import matplotlib.pyplot as plt
import pandas as pd

def gerar_grafico_por_satelite(df: pd.DataFrame) -> None:
    """
    Gera gráfico de barras com focos por satélite
    """
    if df.empty:
        print("DataFrame vazio, não é possível gerar gráfico.")
        return
    
    # Contar por satélite
    contagem = df['satelite'].value_counts()
    
    plt.figure(figsize=(10, 6))
    contagem.plot(kind='bar')
    plt.title('Focos de Queimadas por Satélite')
    plt.xlabel('Satélite')
    plt.ylabel('Número de Focos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Salvar gráfico
    plt.savefig('grafico_por_satelite.png')
    print("Gráfico salvo como 'grafico_por_satelite.png'")
    plt.show()


def gerar_grafico_por_estado(df: pd.DataFrame) -> None:
    """
    Gera gráfico de barras com focos por estado (apenas Brasil)
    """
    if df.empty or 'estado' not in df.columns:
        print("Dados insuficientes para gerar gráfico por estado.")
        return
    
    # Filtrar apenas Brasil
    df_brasil = df[df['pais'].str.contains('Brazil|Brasil', case=False, na=False)]
    
    if df_brasil.empty:
        print("Nenhum foco no Brasil encontrado.")
        return
    
    # Contar por estado
    contagem = df_brasil['estado'].value_counts()
    
    if len(contagem) == 0:
        print("Nenhum estado identificado.")
        return
    
    plt.figure(figsize=(12, 6))
    contagem.plot(kind='bar')
    plt.title('Focos de Queimadas por Estado (Brasil)')
    plt.xlabel('Estado')
    plt.ylabel('Número de Focos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Salvar gráfico
    plt.savefig('grafico_por_estado.png')
    print("Gráfico salvo como 'grafico_por_estado.png'")
    plt.show()