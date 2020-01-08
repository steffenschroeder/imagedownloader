import pytest

from download_images import download_image_to_disk


@pytest.fixture
def target_dir(tmpdir):
    tmpdir.chdir()
    yield tmpdir


def test_download_single_image(target_dir):
    download_image_to_disk("https://httpbin.org/image/jpeg")
    expected_file = target_dir.join("result.jpeg")
    assert expected_file.exists()


@pytest.mark.parametrize("status_code", [404, 500])
def test_download_but_failing(target_dir, status_code):
    download_image_to_disk(f"https://httpbin.org/status/{status_code}")

    assert len(target_dir.listdir()) == 0


def test_download_no_url(target_dir):
    download_image_to_disk("")

    assert len(target_dir.listdir()) == 0
