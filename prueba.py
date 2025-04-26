import asyncio
import json
from datetime import datetime
from scrapfly import ScrapeConfig, ScrapflyClient

SCRAPFLY = ScrapflyClient(key="scp-live-a6b6e347acb448eaa4b211f7f0756e3d")

async def scrape_user_profile(username: str) -> dict:
    """
    Scrapea datos de un perfil de X (Twitter) usando Scrapfly.
    """
    url = f"https://x.com/{username}"
    result = await SCRAPFLY.async_scrape(ScrapeConfig(
        url, 
        render_js=True,
        wait_for_selector="[data-testid='primaryColumn']"
    ))

    _xhr_calls = result.scrape_result["browser_data"]["xhr_call"]
    tweet_call = [f for f in _xhr_calls if "UserBy" in f["url"]]

    for xhr in tweet_call:
        if not xhr["response"]:
            continue
        data = json.loads(xhr["response"]["body"])
        return data['data']['user']['result']

async def loop_scrape(username: str):
    """
    Ejecuta el scraping cada 10 segundos e imprime los datos completos más la hora.
    """
    while True:
        try:
            data = await scrape_user_profile(username)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n===== {now} =====")
            print(json.dumps(data, indent=2, ensure_ascii=False))  # Muestra todo el JSON de forma legible
            print("========================================\n")

        except Exception as e:
            print(f"Error: {e}")
        
        await asyncio.sleep(10)

if __name__ == "__main__":
    print(asyncio.run(scrape_tweet("https://x.com/Scrapfly_dev")))