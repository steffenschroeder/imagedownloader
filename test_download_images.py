from pathlib import Path

import pytest

from download_images import _get_filename_by_url
from download_images import download_image_to_disk
from download_images import download_images_from_files


@pytest.fixture(autouse=True)
def target_dir(tmpdir):
    tmpdir.chdir()
    yield tmpdir


def write_file_with_content(filename, *lines):
    with open(filename, "w") as f:
        for line in lines:
            f.writelines(line + "\n")


def test_download_single_image():
    download_image_to_disk("https://picsum.photos/200.jpg")
    assert_current_folder_contains_files("200.jpg")


@pytest.mark.parametrize("status_code", [404, 500])
def test_download_but_failing(target_dir, status_code):
    download_image_to_disk(f"https://httpbin.org/status/{status_code}")
    assert len(target_dir.listdir()) == 0


def test_download_no_url(target_dir):
    download_image_to_disk("")
    assert len(target_dir.listdir()) == 0


def test_download_from_file():
    write_file_with_content("file1.txt", "https://picsum.photos/200.jpg")

    download_images_from_files(["file1.txt"])

    assert_current_folder_contains_files("file1.txt", "200.jpg")


def test_download_from_multiple_files():
    write_file_with_content(
        "file1.txt", "https://picsum.photos/100.jpg", "https://picsum.photos/200.jpg"
    )
    write_file_with_content(
        "file2.txt", "https://picsum.photos/300.jpg", "https://picsum.photos/400.jpg"
    )

    download_images_from_files(["file1.txt", "file2.txt"])

    assert_current_folder_contains_files(
        "file1.txt", "file2.txt", "100.jpg", "200.jpg", "300.jpg", "400.jpg"
    )


def test_get_filename_by_url():
    assert _get_filename_by_url("https://picsum.photos/200.jpg") == "200.jpg"


def assert_current_folder_contains_files(*filenames):
    file_in_directory = [
        filename.name for filename in Path().glob("*") if filename.is_file()
    ]
    assert set(file_in_directory) == set(filenames)
