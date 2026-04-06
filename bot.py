import sys
import subprocess

def main():
    print("Iniciando o download de dados (Automação web)...")
    download_result = subprocess.run([sys.executable, "src/download_dados.py"])
    
    if download_result.returncode != 0:
        print("Ocorreu um erro durante o download dos dados.")
        sys.exit(download_result.returncode)
    
    print("Iniciando o processamento dos dados e geração dos gráficos...")
    processamento_result = subprocess.run([sys.executable, "src/main.py"])
    
    if processamento_result.returncode != 0:
        print("Ocorreu um erro durante o processamento.")
        sys.exit(processamento_result.returncode)

    print("Processamento concluído com sucesso! (Automação BotCity Finalizada)")

    import os
    import glob
    import shutil
    
    print("Tentando salvar e abrir os arquivos finais...")
    try:

        pasta_destino_github = r"C:\github\monitoramento_queimadas\output"
        
  
        if os.path.exists("output"):
            shutil.copytree("output", pasta_destino_github, dirs_exist_ok=True)
            print("Arquivos salvos com sucesso na pasta C:\\github\\monitoramento_queimadas\\output !")

        caminho_html = os.path.join(pasta_destino_github, "graficos", "mapa_calor_queimadas.html")
        if os.path.exists(caminho_html):
            os.startfile(caminho_html)
        
        arquivos_excel = glob.glob(os.path.join(pasta_destino_github, "dados", "*.xlsx"))
        if arquivos_excel:
            ultimo_excel = max(arquivos_excel, key=os.path.getctime)
            os.startfile(ultimo_excel)
            
    except Exception as e:
        print(f"Erro ao tentar abrir os arquivos gerados: {e}")

if __name__ == '__main__':
    main()
