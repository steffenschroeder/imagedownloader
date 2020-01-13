import logging
import sys

import requests


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file...>")
        sys.exit(1)

    filenames = sys.argv[1:]
    download_images_from_files(filenames)


def download_images_from_files(files):
    for filename in files:
        try:
            with open(filename) as f:
                for url in f:
                    download_image_to_disk(url.strip())
        except FileNotFoundError:
            logging.error(f"File {filename} does not exist")
            pass


def download_image_to_disk(image_url):
    if not image_url:
        return
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


def _get_filename_by_url(url):
    return url.rsplit("/", 1)[-1]


if __name__ == "__main__":
    logging.basicConfig()
    main()
