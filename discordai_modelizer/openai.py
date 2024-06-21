import json
import os

from openai import OpenAI


def list_jobs(openai_key: str, simple=False):
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    client = OpenAI()
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
    client.close()


def list_models(openai_key: str, simple=False):
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    client = OpenAI()
    finetunes = client.models.list()
    if not simple:
        print(json.dumps([f.model_dump() for f in finetunes], indent=4))
    else:
        print(json.dumps([{"id": m.id} for m in finetunes.data], indent=4))
    client.close()


def get_status(openai_key: str, job_id: str, events: bool):
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    client = OpenAI()
    if events:
        print(client.fine_tuning.jobs.list_events(job_id).data)
    else:
        print(client.fine_tuning.jobs.retrieve(job_id))
    client.close()


def cancel_job(openai_key: str, job_id: str):
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    client = OpenAI()
    print(client.fine_tuning.jobs.cancel(job_id))
    client.close()


def delete_model(openai_key: str, model_name: str):
    confirm = input(
        "Are you sure you want to delete this model? This action is not reversable. Y/N: "
    )
    if confirm.lower() not in ["y", "yes"]:
        print("Cancelling model deletion...")
        return
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    client = OpenAI()
    print(client.models.delete(model_name))
    client.close()
