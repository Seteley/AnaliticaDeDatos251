import asyncio
import json

from scrapfly import ScrapeConfig, ScrapflyClient

SCRAPFLY = ScrapflyClient(key="scp-live-a6b6e347acb448eaa4b211f7f0756e3d")

async def scrape_tweet(url: str) -> dict:
    """
    Scrape a X.com profile details e.g.: https://x.com/Scrapfly_dev
    """
    result = await SCRAPFLY.async_scrape(ScrapeConfig(
        url, 
        render_js=True,  # enable headless browser
        wait_for_selector="[data-testid='primaryColumn']"  # wait for page to finish loading 
    ))
    # capture background requests and extract ones that request Tweet data
    _xhr_calls = result.scrape_result["browser_data"]["xhr_call"]
    tweet_call = [f for f in _xhr_calls if "UserBy" in f["url"]]
    for xhr in tweet_call:
        if not xhr["response"]:
            continue
        data = json.loads(xhr["response"]["body"])
        return data['data']['user']['result']

if __name__ == "__main__":
    print(asyncio.run(scrape_tweet("https://x.com/Scrapfly_dev")))