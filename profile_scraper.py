import asyncio
from playwright.async_api import async_playwright


async def get_user_playlists(user_url: str) -> list[str]:
    if not user_url.endswith("/playlists"):
        user_url = user_url.rstrip("/") + "/playlists"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(user_url, timeout=60000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_selector('a[href^="/playlist/"]', timeout=10000)

        prev_count = 0
        links = []

        while True:
            await page.mouse.wheel(0, 5000)
            await page.wait_for_timeout(1000)

            links = await page.eval_on_selector_all(
                'a[href^="/playlist/"]',
                "els => els.map(e => e.getAttribute('href'))"
            )

            if len(links) == prev_count:
                break

            prev_count = len(links)

        await browser.close()

    playlist_urls = sorted(set(
        f"https://open.spotify.com{link.split('?')[0]}"
        for link in links if link
    ))

    return playlist_urls


def get_user_playlists_sync(user_url: str) -> list[str]:
    return asyncio.run(get_user_playlists(user_url))