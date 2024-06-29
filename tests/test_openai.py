import os
import pytest

from re import escape
from io import StringIO
from openai import PermissionDeniedError
from discordai_modelizer import openai as openai_wrapper
from . import expected_values
from .conftest import list_dict_comp


@pytest.fixture(scope="function")
def unset_openai_api_key():
    key = os.environ["OPENAI_API_KEY"]
    del os.environ["OPENAI_API_KEY"]
    yield
    openai_wrapper.set_openai_api_key(key)


def test_model_list():
    models = openai_wrapper.list_models()
    list_dict_comp(expected_values.list_module_expected, models)


def test_model_list_full():
    models = openai_wrapper.list_models(full=True)
    list_dict_comp(expected_values.list_module_expected_full, models)


def test_job_list():
    jobs = openai_wrapper.list_jobs()
    list_dict_comp(expected_values.list_job_expected, jobs)


def test_job_list_full():
    jobs = openai_wrapper.list_jobs(full=True)
    list_dict_comp(expected_values.list_job_expected_full, jobs)


def test_job_info():
    info = openai_wrapper.get_job_info("ftjob-i2IyeV2xbLCSrYq45kTKSdwE")
    assert expected_values.job_info_expected == info


def test_job_events():
    events = openai_wrapper.get_job_events("ftjob-i2IyeV2xbLCSrYq45kTKSdwE")
    list_dict_comp(expected_values.job_events_expected, events)


def test_job_cancel():
    cancel = openai_wrapper.cancel_job("ftjob-i2IyeV2xbLCSrYq45kTKSdwE")
    assert expected_values.job_cancel_expected == cancel


def test_delete_model(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("Y\n"))
    with pytest.raises(
        PermissionDeniedError,
        match="You have insufficient permissions for this operation. Missing scopes: api.delete",
    ):
        openai_wrapper.delete_model("whisper-1")


def test_delete_model_cancel(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("N\n"))
    openai_wrapper.delete_model("whisper-1")
    stdout = capsys.readouterr()
    assert "Cancelling model deletion..." in stdout.out


def test_no_openai_api_key(unset_openai_api_key):
    with pytest.raises(
        ValueError,
        match=escape(
            "Your OpenAI API key must either be passed in as an argument or set as an environment variable"
        ),
    ):
        openai_wrapper.set_openai_api_key(None)
