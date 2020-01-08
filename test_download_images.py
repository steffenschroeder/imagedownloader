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
