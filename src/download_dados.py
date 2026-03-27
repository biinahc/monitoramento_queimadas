from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

URL = "https://terrabrasilis.dpi.inpe.br/queimadas/portal/"
PASTA_DOWNLOAD = Path("data/bruto")
PASTA_DOWNLOAD.mkdir(parents=True, exist_ok=True)


def clicar_card_focos(page):
    seletores = [
        "a.custom-card:has-text('Focos de Queimadas')",
        "text='Focos de Queimadas'",
        "a[href*='da-focos']"
    ]

    for seletor in seletores:
        try:
            locator = page.locator(seletor).first
            locator.wait_for(state="visible", timeout=5000)
            locator.click()
            print("Card clicado.")
            return
        except:
            continue

    raise RuntimeError("Não conseguiu clicar no card.")


def clicar_botao_10min(page):
    seletores = [
        "a[aria-label='10 min']",
        "a[href*='10min']"
    ]

    for seletor in seletores:
        try:
            locator = page.locator(seletor).first
            locator.wait_for(state="visible", timeout=5000)
            locator.click()
            print("Botão 10 min clicado.")
            return
        except:
            continue

    raise RuntimeError("Não conseguiu clicar no botão 10 min.")


def baixar_arquivo_mais_recente(page):
    print("Procurando arquivos CSV...")

    page.wait_for_timeout(3000)

    links_csv = page.locator("a[href$='.csv']")
    total = links_csv.count()

    if total == 0:
        raise RuntimeError("Nenhum CSV encontrado.")

    print(f"{total} arquivos encontrados.")

    ultimo = links_csv.nth(total - 1)

    nome = ultimo.inner_text().strip()
    if not nome:
        nome = "arquivo_queimadas.csv"

    caminho = PASTA_DOWNLOAD / nome

    print(f"Baixando: {nome}")

    with page.expect_download(timeout=60000) as download_info:
        ultimo.click()

    download = download_info.value
    download.save_as(str(caminho))

    print(f"Arquivo salvo em: {caminho}")
    return caminho


def iniciar_automacao():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True, accept_downloads=True)
        page = context.new_page()

        try:
            print("Abrindo portal...")
            page.goto(URL, wait_until="networkidle")

            print("Clicando no card...")
            clicar_card_focos(page)

            page.wait_for_timeout(3000)

            print("Clicando no botão 10 min...")
            clicar_botao_10min(page)

            print("Aguardando nova aba...")
            page.wait_for_timeout(5000)

            # ⚠️ IMPORTANTE: abre nova aba
            pages = context.pages
            if len(pages) > 1:
                page = pages[-1]

            print("Baixando arquivo mais recente...")
            baixar_arquivo_mais_recente(page)

            print("Automação finalizada com sucesso.")

        except PlaywrightTimeoutError:
            print("Erro: tempo excedido.")
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    iniciar_automacao()