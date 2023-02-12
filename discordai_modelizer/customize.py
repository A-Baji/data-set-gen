import os
import subprocess
import appdirs
import shutil
import pathlib

import openai
from discordai_modelizer.gen_dataset import parse_logs, get_lines


def create_model(bot_token: str, openai_key: str, channel_id: str, user_id: str, thought_time=10,
                 max_entry_count=1000, reduce_mode="even", base_model="none", clean=False, redownload=False):
    os.environ["OPENAI_API_KEY"] = openai_key
    channel_user = f"{channel_id}_{user_id}"
    files_path = pathlib.Path(appdirs.user_data_dir(appname="discordai"))
    full_logs_path = files_path / f"{channel_id}_logs.json"
    full_dataset_path = files_path / f"{channel_user}_data_set.jsonl"

    # Download logs
    if not os.path.isfile(full_logs_path) or redownload:
        print("INFO: Exporting chat logs using DiscordChatExporter...")
        print("INFO: This may take a few minutes to hours depending on the message count of the channel")
        print("INFO: Progress will NOT be saved if cancelled")
        print("--------------------------DiscordChatExporter---------------------------")
        DiscordChatExporter = pathlib.Path(os.path.dirname(__file__)) / 'DiscordChatExporter'/ 'DiscordChatExporter.Cli.exe'
        subprocess.run([
            DiscordChatExporter,
            "export",
            "-c", channel_id,
            "-t", bot_token,
            "-o", f"{channel_id}_logs.json",
            "-f", "Json"
        ])
        print("--------------------------DiscordChatExporter---------------------------")
        shutil.move(f"{channel_id}_logs.json", full_logs_path)
        print(f"INFO: Logs saved to {full_logs_path}")
    else:
        print(f"INFO: Chat logs detected locally at {full_logs_path}... Skipping download.")

    # Parse logs
    print("INFO: Parsing chat logs into an openAI compatible dataset...")
    parse_logs(full_logs_path, channel_id, user_id, thought_time)
    get_lines(full_dataset_path, max_entry_count, reduce_mode)

    # Train customized openAI model
    if base_model in ["davinci", "curie", "babbage", "ada"]:
        print("INFO: Training customized openAI model...")
        upload_response = openai.File.create(api_key=openai_key,
            file=open(full_dataset_path, "rb"),
            purpose='fine-tune'
        )
        file_id = upload_response.id
        fine_tune=openai.FineTune.create(api_key=openai_key, training_file=file_id, model=base_model, suffix=user_id)
        print(f"INFO: Fine tune job id: {fine_tune.id}")
        print("INFO: This may take a few minutes to hours depending on the size of the dataset and the selected base model")
        print("INFO: Use the `job status` command to check on the status of job process") 
        print("INFO: If you are using the python package, or have the `openai` python package installed, you can instead use the `job follow` command to follow the event stream of the job.")
    elif base_model == "none":
        print("INFO: No base model selected... Skipping training.")

    # Clean up generated files
    if clean:
        try:
            os.remove(full_dataset_path)
        except FileNotFoundError:
            pass
