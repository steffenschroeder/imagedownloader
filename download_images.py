import argparse
import asyncio
import logging

import aiohttp


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        nargs="+",
        type=str,
        help="File containing Images URLs to download. One URL per line",
    )
    args = parser.parse_args()

    filenames = args.file
    await download_images_from_files(filenames)


async def download_images_from_files(filesnames):
    urls = []
    for filename in filesnames:
        try:
            with open(filename) as file_with_urls:
                for url in file_with_urls:
                    urls.append(url.strip())

        except FileNotFoundError:
            logging.error(f"File {filename} does not exist")
            pass

    coroutines = [download_image_to_disk(url) for url in urls]
    await asyncio.gather(*coroutines)


async def download_image_to_disk(image_url):
    if not image_url:
        return
    if not _is_jpeg_url(image_url):
        logging.error(
            f"URL {image_url} is not a jpeg (does not end with .jpg or .jpeg)"
        )

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                name = _get_filename_by_url(image_url)
                with open(name, "wb") as result_file:
                    result_file.write(await response.read())
            elif response.status == 400:
                logging.warning(f"Image {image_url} does not exist")
            else:
                logging.warning(
                    f"Image {image_url} cannot be downloaded (HTTP Status: {response.status})"
                )


def _is_jpeg_url(url):
    return url and url.endswith(".jpg") or url.endswith(".jpeg")


def _get_filename_by_url(url):
    return url.rsplit("/", 1)[-1]


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(main())
