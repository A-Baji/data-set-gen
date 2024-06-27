import json
import os

from openai import OpenAI
from datetime import datetime, timezone


def convert_timestamp(time: int):
    timestamp = datetime.fromtimestamp(time, tz=timezone.utc)
    human_readable_time = timestamp.astimezone().strftime("%Y-%m-%d %H:%M:%S")
    return human_readable_time


def convert_in_place(obj, key: str):
    obj[key] = convert_timestamp(obj[key])
    return obj


def list_jobs(openai_key: str, full=False) -> list[dict]:
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    client = OpenAI()
    finetunes = client.fine_tuning.jobs.list()
    client.close()
    if full:
        return [
            convert_in_place(
                (
                    convert_in_place(j.model_dump(), "finished_at")
                    if j.finished_at
                    else j.model_dump()
                ),
                "created_at",
            )
            for j in finetunes.data
        ]
    else:
        return [
            {
                "id": j.id,
                "model": j.model,
                "status": j.status,
                "created_at": convert_timestamp(j.created_at),
                "finished_at": (
                    convert_timestamp(j.finished_at) if j.finished_at else None
                ),
            }
            for j in finetunes.data
        ]


def list_models(openai_key: str, full=False) -> list[dict]:
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    client = OpenAI()
    finetunes = client.models.list()
    client.close()
    if full:
        return [convert_in_place(f.model_dump(), "created") for f in finetunes.data]
    else:
        return [
            {"id": m.id, "created": convert_timestamp(m.created)}
            for m in finetunes.data
        ]


def get_job_info(openai_key: str, job_id: str) -> dict:
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    client = OpenAI()
    job = client.fine_tuning.jobs.retrieve(job_id)
    client.close()
    return convert_in_place(
        (
            convert_in_place(job.model_dump(), "finished_at")
            if job.finished_at
            else job.model_dump()
        ),
        "created_at",
    )


def get_job_events(openai_key: str, job_id: str) -> list[dict]:
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    client = OpenAI()
    events = client.fine_tuning.jobs.list_events(job_id).data
    client.close()
    return [
        convert_in_place(
            j.model_dump(),
            "created_at",
        )
        for j in events
    ]


def cancel_job(openai_key: str, job_id: str) -> dict:
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    client = OpenAI()
    client.fine_tuning.jobs.cancel(job_id)
    client.close()
    return {"result": f"Canceled fine-tuning job: {job_id}"}


def delete_model(openai_key: str, model_name: str) -> dict:
    confirm = input(
        "Are you sure you want to delete this model? This action is not reversable. Y/N: "
    )
    if confirm.lower() not in ["y", "yes"]:
        print("Cancelling model deletion...")
        return
    os.environ["OPENAI_API_KEY"] = openai_key or os.environ["OPENAI_API_KEY"]
    client = OpenAI()
    deleted = client.models.delete(model_name).model_dump()
    client.close()
    return deleted
