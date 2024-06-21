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


def get_status(openai_key: str, job_id: str, events: bool):
    if events:
        print(client.fine_tuning.jobs.list_events(job_id).data)
    else:
        print(client.fine_tuning.jobs.retrieve(job_id))


def cancel_job(openai_key: str, job_id: str):
    print(client.fine_tunes.cancel(job_id, openai_key))


def delete_model(openai_key: str, model_name: str):
    confirm = input(
        "Are you sure you want to delete this model? This action is not reversable. Y/N: "
    )
    if confirm.lower() not in ["y", "yes"]:
        print("Cancelling model deletion...")
        return
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    print(client.models.delete(model_name))
