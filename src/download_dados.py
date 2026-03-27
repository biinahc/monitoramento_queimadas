from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


URL_PORTAL = "https://terrabrasilis.dpi.inpe.br/queimadas/portal/"
PASTA_DOWNLOAD = Path("data/bruto")


XPATH_CARD = "/html/body/main/div[2]/div[2]/div[1]/a/div"
XPATH_BOTAO_DOWNLOAD = '//*[@id="da-focos"]/div/div/div[1]/div[2]/div/div[1]/a'


def garantir_pasta_download() -> None:
    PASTA_DOWNLOAD.mkdir(parents=True, exist_ok=True)


def baixar_arquivo_mais_recente(headless: bool = False) -> Path:
    garantir_pasta_download()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            print("Abrindo portal de queimadas...")
            page.goto(URL_PORTAL, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)

            print("Clicando no card...")
            page.locator(f"xpath={XPATH_CARD}").click(timeout=10000)
            page.wait_for_timeout(3000)

            print("Clicando no botão de download...")
            page.locator(f"xpath={XPATH_BOTAO_DOWNLOAD}").click(timeout=10000)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(5000)

            print("Localizando os arquivos CSV...")
            links_csv = page.locator("a[href$='.csv']")

            quantidade = links_csv.count()
            if quantidade == 0:
                raise RuntimeError("Nenhum arquivo CSV foi encontrado na página.")

            print(f"Foram encontrados {quantidade} arquivos. Selecionando o último...")

            ultimo_link = links_csv.nth(quantidade - 1)

            nome_arquivo = ultimo_link.inner_text().strip()
            if not nome_arquivo:
                nome_arquivo = f"arquivo_queimadas_{quantidade}.csv"

            caminho_final = PASTA_DOWNLOAD / nome_arquivo

            print(f"Baixando: {nome_arquivo}")

            with page.expect_download(timeout=60000) as download_info:
                ultimo_link.click()

            download = download_info.value
            download.save_as(str(caminho_final))

            print(f"Arquivo salvo em: {caminho_final}")
            return caminho_final

        except PlaywrightTimeoutError:
            raise RuntimeError("Tempo excedido durante a automação.")
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    try:
        arquivo = baixar_arquivo_mais_recente(headless=False)
        print(f"Download concluído com sucesso: {arquivo}")
    except Exception as erro:
        print(f"Erro na automação: {erro}")