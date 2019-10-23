import asyncio
import aiohttp
from typing import TextIO
from tqdm import tqdm
URL = ""
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


async def fetch(session: aiohttp.ClientSession,
                semaphore: asyncio.BoundedSemaphore,
                pbar: tqdm,
                url: str, failed: TextIO):
    async with semaphore:
        async with session.get(url) as response:
            status = response.status
            content = await response.content.read()
            if status != 200:
                failed.write(url + '\n')
                failed.flush()

            fn = url.rsplit("/")[-1]
            with open(fn, 'wb') as out:
                out.write(content)
        pbar.update(1)


async def main():
    jobs = []
    asyncio_semaphore = asyncio.BoundedSemaphore(20)
    async with aiohttp.ClientSession() as session:
        with open('urls.txt', 'r') as fp, open("remains.txt", 'a') as failed:
            lines = set(x.rstrip('\n').strip('"') for x in fp)
            pbar = tqdm(total=len(lines))
            for url in lines:
                jobs.append(asyncio.ensure_future(fetch(session, asyncio_semaphore, pbar, url, failed)))
            await asyncio.gather(*jobs)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(main())