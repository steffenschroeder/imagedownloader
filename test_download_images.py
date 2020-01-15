from pathlib import Path

import pytest

from download_images import _get_filename_by_url
from download_images import _is_jpeg_url
from download_images import download_image_to_disk
from download_images import download_images_from_files


@pytest.fixture(autouse=True)
def target_dir(tmpdir):
    tmpdir.chdir()
    yield tmpdir


def write_file_with_content(filename, *lines):
    """
    writes ``lines`` to file with name  ``filename``
    :param filename: name of the file to write
    :param lines: lines to write to that file
    :return:
    """
    with open(filename, "w") as f:
        for line in lines:
            f.writelines(line + "\n")


def assert_current_folder_contains_files(*filenames):
    """
    asserts the the current folder contains exactly the files mentioned in filenames
    :param filenames: files to be present in the current folder
    :return:
    """
    file_in_directory = [
        filename.name for filename in Path().glob("*") if filename.is_file()
    ]
    assert set(file_in_directory) == set(filenames)


@pytest.mark.asyncio
async def test_download_single_image():
    await download_image_to_disk("https://picsum.photos/200.jpg")
    assert_current_folder_contains_files("200.jpg")


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [404, 500])
async def test_download_but_failing(target_dir, status_code):
    await download_image_to_disk(f"https://httpbin.org/status/{status_code}")
    assert len(target_dir.listdir()) == 0


@pytest.mark.asyncio
async def test_download_no_url(target_dir):
    await download_image_to_disk("")
    assert len(target_dir.listdir()) == 0


@pytest.mark.asyncio
async def test_download_from_file():
    write_file_with_content("file1.txt", "https://picsum.photos/200.jpg")

    await download_images_from_files(["file1.txt"])

    assert_current_folder_contains_files("file1.txt", "200.jpg")


@pytest.mark.asyncio
async def test_download_from_non_existing_file():
    await download_images_from_files(["nonexisting.txt"])

    # output folder contains no extra files, no error is thrown
    assert_current_folder_contains_files()


@pytest.mark.asyncio
async def test_download_from_multiple_files():
    write_file_with_content(
        "file1.txt", "https://picsum.photos/100.jpg", "https://picsum.photos/200.jpg"
    )
    write_file_with_content(
        "file2.txt", "https://picsum.photos/300.jpg", "https://picsum.photos/400.jpg"
    )

    await download_images_from_files(["file1.txt", "file2.txt"])

    assert_current_folder_contains_files(
        "file1.txt", "file2.txt", "100.jpg", "200.jpg", "300.jpg", "400.jpg"
    )


def test_get_filename_by_url():
    assert _get_filename_by_url("https://picsum.photos/200.jpg") == "200.jpg"


@pytest.mark.parametrize(
    "url, expected",
    [
        ["", False],
        ["https://www.google.com", False],
        ["https://totalcommander.ch/win/tcmd922ax64.exe", False],
        ["https://picsum.photos/200.jpg", True],
        ["https://picsum.photos/200.jpeg", True],
    ],
)
def test_url_is_jpeg(url, expected):
    assert _is_jpeg_url(url) == expected
