import asyncio
import aiohttp
import aiofiles
import argparse

TIMEOUT_TIME = 0.51  # AVG value for seeing print statements about timing


async def get_urls_from_file(file_path: str):
    async with aiofiles.open(file_path, 'r') as file:
        urls = [line.strip() for line in await file.readlines()]
    return urls


async def save_to_file(content: str, file_number: int):
    file_name = f"page_{file_number}.html"
    async with aiofiles.open(file_name, 'w') as file:
        await file.write(content)


async def get_information_from_url(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            return await response.text()


async def get_information_from_url_with_timeout(url: str, file_number: int):
    try:
        async with asyncio.timeout(TIMEOUT_TIME):
            html_content = await get_information_from_url(url)
        await save_to_file(html_content, file_number)
    except asyncio.TimeoutError:
        print("Getting information from url timed out, moving on...")


async def test1(file_path: str):
    """Default, with one cycle"""
    urls = await get_urls_from_file(file_path)
    tasks = [get_information_from_url_with_timeout(url, number) for number, url in enumerate(urls)]
    await asyncio.gather(*tasks)


async def test2(file_path: str):
    """With ten cycles, sometimes we can see print statements about timed out, but be careful with that test :)."""
    urls = await get_urls_from_file(file_path)
    tasks = [get_information_from_url_with_timeout(url, number) for number, url in enumerate(urls * 10)]
    await asyncio.gather(*tasks)


async def main(file_path: str):
    await test1(file_path)
    # await test2(file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch URLs and save content to files.")
    parser.add_argument("file_path", help="Path to the file containing URLs")
    args = parser.parse_args()

    asyncio.run(main(args.file_path))
