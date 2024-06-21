from openai import OpenAI

client = OpenAI()
import json
import os
import subprocess


def list_jobs(openai_key: str, simple=False):
    finetunes = client.fine_tuning.jobs.list()
    if not simple:
        print(json.dumps(finetunes.data))
    else:
        print(
            json.dumps(
                [
                    {
                        "fine_tuned_model": j.fine_tuned_model,
                        "id": j.id,
                        "status": j.status,
                    }
                    for j in finetunes.data
                ],
                indent=4,
            )
        )


def list_models(openai_key: str, simple=False):
    finetunes = client.models.list()
    if not simple:
        print(json.dumps([f.model_dump() for f in finetunes], indent=4))
    else:
        print(json.dumps([{"id": m.id} for m in finetunes.data], indent=4))


def follow_job(openai_key: str, job_id: str):
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    try:
        subprocess.run([
            "openai", "api", "fine_tunes.follow",
            "-i", job_id
        ])
    except FileNotFoundError:
        print("ERROR: You must have the `openai` python package installed to use this command.")


def get_status(openai_key: str, job_id: str, events: bool):
    status = openai.FineTune.retrieve(job_id, openai_key)
    if events:
        print(status["events"])
    else:
        print(status)


def cancel_job(openai_key: str, job_id: str):
    print(openai.FineTune.cancel(job_id, openai_key))


def delete_model(openai_key: str, model_name: str):
    confirm = input("Are you sure you want to delete this model? This action is not reversable. Y/N: ")
    if confirm not in ["Y", "y", "yes", "Yes", "YES"]:
        print("Cancelling model deletion...")
        return
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    print(openai.Model.delete(model_name))
