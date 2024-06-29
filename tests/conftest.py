import os
import pathlib
import appdirs
import pytest

from discordai_modelizer import customize
from discordai_modelizer.openai import set_openai_api_key


CHANNEL_ID = os.environ["CHANNEL_ID"]
USER = os.environ["USERNAME"]
FILES_PATH = pathlib.Path(appdirs.user_data_dir(appname="discordai"))
FULL_LOGS_PATH = FILES_PATH / f"{CHANNEL_ID}_logs.json"
FULL_DATASET_PATH = FILES_PATH / f"{CHANNEL_ID[:4]}_{USER}_data_set.jsonl"


def list_dict_comp(x, y):
    assert len(x) == len(y)
    for d1, d2 in zip(x, y):
        assert d1 == d2


@pytest.fixture(scope="session")
def default_file_output():
    # Ensure a clean start by removing any existing files
    if FULL_LOGS_PATH.exists():
        FULL_LOGS_PATH.unlink()
    if FULL_DATASET_PATH.exists():
        FULL_DATASET_PATH.unlink()
    # Generate log and dataset files
    customize.create_model(CHANNEL_ID, USER)
    yield
    # Cleanup after the tests in this module
    if FULL_LOGS_PATH.exists():
        FULL_LOGS_PATH.unlink()
    if FULL_DATASET_PATH.exists():
        FULL_DATASET_PATH.unlink()


@pytest.fixture(scope="function")
def set_bad_openai_key():
    key = os.environ["OPENAI_API_KEY"]
    set_openai_api_key("BAD_KEY")
    yield
    set_openai_api_key(key)
