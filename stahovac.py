import asyncio
import os
import urllib.parse
import shutil
from datetime import datetime
from playwright.async_api import async_playwright

async def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # 1. Složka pro dočasné stažení jednotlivých PDF letáků
    slozky_nazev = os.path.join(dir_path, "letaky_temp") 
    os.makedirs(slozky_nazev, exist_ok=True)
    
    dnes = datetime.now().strftime("%Y-%m-%d")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        async def stahni_url(url, jmeno_obchodu):
            if url:
                print(f"[{jmeno_obchodu}] Stahuji z: {url}")
                resp = await context.request.get(url)
                if resp.ok:
                    cesta = f"{slozky_nazev}/{jmeno_obchodu}_{dnes}.pdf"
                    with open(cesta, 'wb') as f:
                        f.write(await resp.body())
                    print(f"✅ [{jmeno_obchodu}] Uloženo: {cesta}\n")

        # --- GLOBUS ---
        print("Hledám Globus...")
        g_page = await context.new_page()
        await g_page.goto("https://www.globus.cz/olomouc/letaky", wait_until="domcontentloaded")
        try:
            odkaz = await g_page.locator('a[aria-label="Stáhnout leták"]').first.get_attribute("href")
            await stahni_url(urllib.parse.urljoin("https://www.globus.cz", odkaz), "Globus")
        except Exception as e:
            print(f"❌ Globus selhal: {e}\n")
        finally:
            await g_page.close()

        # --- KAUFLAND ---
        print("Hledám Kaufland...")
        k_page = await context.new_page()
        await k_page.goto("https://prodejny.kaufland.cz/letak.html", wait_until="domcontentloaded")
        try:
            await k_page.locator('#onetrust-accept-btn-handler, button:has-text("Přijmout")').first.click(timeout=3000)
            await k_page.wait_for_timeout(1000)
        except:
            pass
        try:
            element = k_page.locator('div[data-download-url]').first
            odkaz = await element.get_attribute("data-download-url")
            await stahni_url(odkaz, "Kaufland")
        except Exception as e:
            print(f"❌ Kaufland selhal: {e}\n")
        finally:
            await k_page.close()

        # --- JIP ---
        print("Hledám JIP...")
        j_page = await context.new_page()
        j_page.set_default_timeout(30000)
        await j_page.goto("https://www.jip-potraviny.cz/akcni-letaky/", wait_until="domcontentloaded")
        
        try:
            await j_page.locator('button:has-text("Souhlasím"), button:has-text("Přijmout")').first.click(timeout=5000)
            await j_page.wait_for_timeout(1000)
        except:
            pass

        try:
            print("Vybírám leták Svět potravin...")
            odkaz_letak = j_page.locator('a.i-leaflet__heading-link:has-text("Svět potravin")').first
            
            async with j_page.expect_navigation(timeout=15000):
                await odkaz_letak.click()

            await j_page.wait_for_load_state("domcontentloaded")
            await j_page.wait_for_timeout(3000)

            async with j_page.expect_download(timeout=15000) as download_info:
                await j_page.locator('.button.right:has-text("Download")').first.click()
            
            download = await download_info.value
            cesta_jip = f"{slozky_nazev}/JIP_{dnes}.pdf"
            await download.save_as(cesta_jip)
            print(f"✅ [JIP] Uloženo: {cesta_jip}\n")
        except Exception as e:
            print(f"❌ JIP selhal: {e}\n")
        finally:
            await j_page.close()

        await context.close()
        await browser.close()

    # ZABALENÍ A ÚKLID
    # ZIP se generuje do kořenové složky projektu (přímo pod absent-atmosphere/letaky.zip)
    # Odsud ho v dalším kroku vyzvedne Bash skript přes wrangler r2
    zip_cesta = os.path.join(dir_path, "letaky")
    shutil.make_archive(zip_cesta, 'zip', slozky_nazev)
    
    # Smazání dočasné složky s PDF soubory
    shutil.rmtree(slozky_nazev)
    print(f"📦 Hotovo. Vše zabaleno do souboru {zip_cesta}.zip a dočasná složka byla uklizena.")

if __name__ == "__main__":
    asyncio.run(main())