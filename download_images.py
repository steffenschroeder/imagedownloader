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
    if response.ok:
        with open("result.jpeg", "wb") as result_file:
            result_file.write(response.content)
    elif response.status_code == 404:
        print(f"Image {image_url} does not exist", file=sys.stderr)
    else:
        print(
            f"Image {image_url} cannot be downloaded (HTTP Status: {response.status_code})",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
