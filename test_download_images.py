import pytest

from download_images import _get_filename_by_url
from download_images import download_image_to_disk
from download_images import download_images_from_files


@pytest.fixture
def target_dir(tmpdir):
    tmpdir.chdir()
    yield tmpdir


@pytest.fixture
def a_file(target_dir):
    target_file_path = target_dir.join("file1.txt")
    with open(target_file_path, "w") as f:
        yield f


@pytest.fixture
def b_file(target_dir):
    target_file_path = target_dir.join("file2.txt")
    with open(target_file_path, "w") as f:
        yield f


def test_download_single_image(target_dir):
    download_image_to_disk("https://picsum.photos/200.jpg")
    assert len(target_dir.listdir()) == 1


@pytest.mark.parametrize("status_code", [404, 500])
def test_download_but_failing(target_dir, status_code):
    download_image_to_disk(f"https://httpbin.org/status/{status_code}")
    assert len(target_dir.listdir()) == 0


def test_download_no_url(target_dir):
    download_image_to_disk("")
    assert len(target_dir.listdir()) == 0


def test_download_from_file(target_dir, a_file):
    print("https://picsum.photos/200.jpg", file=a_file, flush=True)
    download_images_from_files(["file1.txt"])
    assert len(target_dir.listdir()) == 2


def test_download_from_multiple_files(target_dir, a_file, b_file):
    print("https://picsum.photos/200.jpg", file=a_file, flush=True)
    print("https://picsum.photos/300.jpg", file=a_file, flush=True)
    print("https://picsum.photos/150.jpg", file=b_file, flush=True)
    print("https://picsum.photos/50.jpg", file=b_file, flush=True)
    download_images_from_files(["file1.txt", "file2.txt"])
    assert len(target_dir.listdir()) == 6


def test_get_filename_by_url():
    assert _get_filename_by_url("https://picsum.photos/200.jpg") == "200.jpg"
