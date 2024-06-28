from discordai_modelizer import openai
from . import expected_values


def list_dict_comp(x, y):
    assert sorted(x, key=lambda x: sorted(x.items())) == sorted(
        y, key=lambda x: sorted(x.items())
    )


def dict_comp(x, y):
    return sorted(x) == sorted(y)


def test_model_list():
    models = openai.list_models()
    list_dict_comp(expected_values.list_module_expected, models)


def test_model_list_full():
    models = openai.list_models(full=True)
    list_dict_comp(expected_values.list_module_expected_full, models)


def test_job_list():
    jobs = openai.list_jobs()
    list_dict_comp(expected_values.list_job_expected, jobs)


def test_job_list_full():
    jobs = openai.list_jobs(full=True)
    list_dict_comp(expected_values.list_job_expected_full, jobs)


def test_job_info():
    info = openai.get_job_info("ftjob-i2IyeV2xbLCSrYq45kTKSdwE")
    dict_comp(expected_values.job_info_expected, info)


def test_job_events():
    events = openai.get_job_events("ftjob-i2IyeV2xbLCSrYq45kTKSdwE")
    list_dict_comp(expected_values.job_events_expected, events)


def test_job_cancel():
    cancel = openai.cancel_job("ftjob-i2IyeV2xbLCSrYq45kTKSdwE")
    dict_comp(expected_values.job_cancel_expected, cancel)
