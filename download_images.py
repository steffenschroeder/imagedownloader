import argparse
import logging

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        nargs="+",
        type=str,
        help="File containing Images URLs to download. One URL per line",
    )
    args = parser.parse_args()

    filenames = args.file
    download_images_from_files(filenames)


def download_images_from_files(filesnames):
    for filename in filesnames:
        try:
            with open(filename) as file_with_urls:
                for url in file_with_urls:
                    download_image_to_disk(url.strip())
        except FileNotFoundError:
            logging.error(f"File {filename} does not exist")
            pass


def download_image_to_disk(image_url):
    if not image_url:
        return
    if not _is_jpeg_url(image_url):
        logging.error(
            f"URL {image_url} is not a jpeg (does not end with .jpg or .jpeg)"
        )
    try:
        response = requests.get(image_url)
    except requests.RequestException as e:
        logging.warning(f"Image {image_url} cannot be downloaded (Exception: {e})")
        return
    if response.ok:
        name = _get_filename_by_url(image_url)
        with open(name, "wb") as result_file:
            result_file.write(response.content)
    elif response.status_code == 404:
        logging.warning(f"Image {image_url} does not exist")
    else:
        logging.warning(
            f"Image {image_url} cannot be downloaded (HTTP Status: {response.status_code})"
        )


def _is_jpeg_url(url):
    return url and url.endswith(".jpg") or url.endswith(".jpeg")


def _get_filename_by_url(url):
    return url.rsplit("/", 1)[-1]


if __name__ == "__main__":
    logging.basicConfig()
    main()
