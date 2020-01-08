import sys

import requests


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <image url>")
        sys.exit(1)

    image_url = sys.argv[1]
    download_image_to_disk(image_url)


def download_image_to_disk(image_url):
    response = requests.get(image_url)
    with open("result.jpeg", "wb") as result_file:
        result_file.write(response.content)


if __name__ == "__main__":
    main()
