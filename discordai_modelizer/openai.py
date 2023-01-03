import openai
import json
import os
import subprocess


def list_jobs(openai_key: str, simple=False):
    finetunes = openai.FineTune.list(openai_key)
    if not simple:
        print(finetunes)
    else:
        simplified = []
        for ft in finetunes["data"]:
            entry = {}
            entry["fine_tuned_model"] = ft["fine_tuned_model"]
            entry["id"] = ft["id"]
            entry["status"] = ft["status"]
            simplified.append(entry)
        print(json.dumps(simplified, indent=4))


def list_models(openai_key: str, simple=False):
    finetunes = openai.Model.list(openai_key)
    if not simple:
        print(finetunes)
    else:
        simplified = []
        for ft in finetunes["data"]:
            entry = {}
            entry["id"] = ft["id"]
            simplified.append(entry)
        print(json.dumps(simplified, indent=4))


def follow_job(openai_key: str, job_id: str):
    os.environ["OPENAI_API_KEY"] = openai_key
    subprocess.run([
        "openai", "api", "fine_tunes.follow",
        "-i", job_id
    ])


def get_status(openai_key: str, job_id: str):
    print(openai.FineTune.retrieve(job_id, openai_key))


def cancel_job(openai_key: str, job_id: str):
    print(openai.FineTune.cancel(job_id, openai_key))


def delete_model(openai_key: str, model_name: str):
    os.environ["OPENAI_API_KEY"] = openai_key
    print(openai.Model.delete(model_name))
