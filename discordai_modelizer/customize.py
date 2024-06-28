import os
import subprocess
import appdirs
import shutil
import pathlib

from openai import OpenAI
from argparse import ArgumentError
from discordai_modelizer.gen_dataset import parse_logs, get_lines
from discordai_modelizer.openai import set_openai_api_key

MODEL_MAP = {
    "davinci": "davinci-002",
    "babbage": "babbage-002",
}


def create_model(
    channel_id: str,
    user_id: str,
    bot_token: str = None,
    openai_key: str = None,
    thought_time=10,
    thought_max: int = None,
    thought_min=4,
    max_entry_count=1000,
    offset="start",
    select_mode="sequential",
    base_model="none",
    reverse=False,
    clean=False,
    redownload=False,
    use_existing=False,
):
    set_openai_api_key(openai_key)
    client = OpenAI()
    channel_user = f"{channel_id[:4]}_{user_id}"
    files_path = pathlib.Path(appdirs.user_data_dir(appname="discordai"))
    full_logs_path = files_path / f"{channel_id}_logs.json"
    full_dataset_path = files_path / f"{channel_user}_data_set.jsonl"

    if not os.path.isfile(full_dataset_path) and use_existing:
        print("ERROR: No existing dataset could be found!")
        return

    # Download logs
    if (not os.path.isfile(full_logs_path) or redownload) and not use_existing:
        try:
            bot_token = bot_token or os.environ["DISCORD_BOT_TOKEN"]
        except KeyError:
            raise ArgumentError(
                None,
                "Your Discord bot token must either be passed in as an argument or set as an environment variable",
            )

        print("INFO: Exporting chat logs using DiscordChatExporter...")
        print(
            "INFO: This may take a few minutes to hours depending on the message count of the channel"
        )
        print("INFO: Progress will NOT be saved if cancelled")
        print(
            "--------------------------DiscordChatExporter---------------------------"
        )
        DiscordChatExporter = (
            pathlib.Path(os.path.dirname(__file__))
            / "DiscordChatExporter"
            / "DiscordChatExporter.Cli"
        )
        subprocess.run(
            [
                DiscordChatExporter,
                "export",
                "-c",
                channel_id,
                "-t",
                bot_token,
                "-o",
                f"{channel_id}_logs.json",
                "-f",
                "Json",
                "--fuck-russia",
                "True",
            ]
        )
        print(
            "--------------------------DiscordChatExporter---------------------------"
        )
        os.makedirs(os.path.dirname(full_logs_path), exist_ok=True)
        shutil.move(f"{channel_id}_logs.json", full_logs_path)
        print(f"INFO: Logs saved to {full_logs_path}")
    elif (os.path.isfile(full_logs_path) and not redownload) and not use_existing:
        print(
            f"INFO: Chat logs detected locally at {full_logs_path}... Skipping download."
        )

    # Parse logs
    if use_existing:
        print("INFO: Using existing dataset... Skipping download and parsing.")
    else:
        print("INFO: Parsing chat logs into an openAI compatible dataset...")
        parse_logs(
            full_logs_path,
            channel_id,
            user_id,
            thought_time,
            thought_max,
            thought_min,
        )
        get_lines(full_dataset_path, max_entry_count, offset, select_mode, reverse)
        if not clean:
            print(f"INFO: Dataset saved to {full_dataset_path}")

    # Train customized openAI model
    if base_model in ["davinci", "babbage"]:
        print("INFO: Starting OpenAI fine-tune job...")
        upload_response = client.files.create(
            file=open(full_dataset_path, "rb"), purpose="fine-tune"
        )
        fine_tune = client.fine_tuning.jobs.create(
            model=MODEL_MAP[base_model],
            training_file=upload_response.id,
            suffix=channel_user[:18],
        )
        print(
            "INFO: This may take a few minutes to hours depending on the size of the dataset and the selected base model"
        )
        print(f"INFO: Fine tune job id: {fine_tune.id}")
        print(
            "INFO: Use the `job info -j <job_id>` command to check the info of the job process"
        )
        print(
            "INFO: Use the `job events -j <job_id>` command to view the fine-tuning events of the job process"
        )
        print(
            "INFO: Use the `job cancel -j <job_id>` command to cancel the job process"
        )
        print(
            "INFO: Or visit the OpenAI dashboard: https://platform.openai.com/finetune"
        )
    else:
        print("INFO: No base model selected... Skipping training.")

    # Clean up generated files
    if clean and not use_existing:
        full_dataset_path.unlink()

    client.close()
