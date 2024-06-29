import os
from openai import AuthenticationError
import pytest

from json import load
from discordai_modelizer import customize
from discordai_modelizer.openai import set_openai_api_key
from . import expected_values
from .conftest import FULL_LOGS_PATH, FULL_DATASET_PATH, CHANNEL_ID, USER


@pytest.fixture(scope="function")
def set_bad_openai_key():
    key = os.environ["OPENAI_API_KEY"]
    set_openai_api_key("BAD_KEY")
    yield
    set_openai_api_key(key)


@pytest.fixture(scope="function")
def unset_bot_token_key():
    key = os.environ["DISCORD_BOT_TOKEN"]
    del os.environ["DISCORD_BOT_TOKEN"]
    yield
    customize.set_bot_token(key)


def test_logs_download(default_file_output):
    assert FULL_LOGS_PATH.exists()
    with open(FULL_LOGS_PATH, "r", encoding="utf-8") as data_file:
        data = load(data_file)
    del data["exportedAt"]
    assert expected_values.channel_logs_expected == data


def test_logs_existing(capsys, default_file_output):
    customize.create_model(CHANNEL_ID, USER)
    stdout = capsys.readouterr()
    assert (
        f"INFO: Chat logs detected locally at {FULL_LOGS_PATH}... Skipping download."
        in stdout.out
    )


def test_use_existing(capsys, default_file_output):
    # Ensure the dataset file exists before running the test
    if not FULL_DATASET_PATH.exists():
        FULL_DATASET_PATH.touch()
    customize.create_model(CHANNEL_ID, USER, use_existing=True)
    stdout = capsys.readouterr()
    assert (
        "INFO: Using existing dataset... Skipping download and parsing." in stdout.out
    )


def test_use_existing_fail(capsys, default_file_output):
    if FULL_DATASET_PATH.exists():
        FULL_DATASET_PATH.unlink()
    customize.create_model(CHANNEL_ID, USER, use_existing=True)
    stdout = capsys.readouterr()
    assert "ERROR: No existing dataset could be found!" in stdout.out


def test_not_use_existing(capsys, default_file_output):
    customize.create_model(CHANNEL_ID, USER, use_existing=False)
    stdout = capsys.readouterr()
    assert "INFO: Parsing chat logs into an openAI compatible dataset..." in stdout.out


def test_not_use_existing_dirty(capsys, default_file_output):
    customize.create_model(CHANNEL_ID, USER, use_existing=False, clean=False)
    stdout = capsys.readouterr()
    assert f"INFO: Dataset saved to {FULL_DATASET_PATH}" in stdout.out


def test_training(capsys, default_file_output, set_bad_openai_key):
    set_openai_api_key("BAD_KEY")
    with pytest.raises(AuthenticationError):
        customize.create_model(CHANNEL_ID, USER, base_model="babbage")
    stdout = capsys.readouterr()
    assert "INFO: Starting OpenAI fine-tune job..." in stdout.out


def test_skip_training(capsys, default_file_output):
    customize.create_model(CHANNEL_ID, USER, base_model="none")
    stdout = capsys.readouterr()
    assert "INFO: No base model selected... Skipping training." in stdout.out


def test_cleanup(default_file_output):
    customize.create_model(CHANNEL_ID, USER, clean=True)
    assert not FULL_DATASET_PATH.exists()


def test_no_bot_token(unset_bot_token_key):
    with pytest.raises(
        ValueError,
        match="Your Discord bot token must either be passed in as an argument or set as an environment variable",
    ):
        customize.set_bot_token(None)
