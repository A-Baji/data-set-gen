import os
import subprocess
import appdirs
import shutil
import pathlib

from discordai_modelizer.gen_dataset import parse_logs, get_lines


def create_model(bot_token: str, openai_key: str, channel_id: str, user_id: str, thought_time=10,
                 max_entry_count=1000, reduce_mode="even", base_model="none", clean=False, redownload=False):
    os.environ["OPENAI_API_KEY"] = openai_key
    channel_user = f"{channel_id}_{user_id}"
    files_path = pathlib.Path(appdirs.user_data_dir(appname="discordai"))
    full_logs_path = files_path / f"{channel_id}_logs.json"
    full_dataset_path = files_path / f"{channel_user}_data_set.jsonl"
    full_prepped_dataset_path = files_path / f"{channel_user}_data_set_prepared.jsonl"

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

    # Prepare and reduce dataset
    print("INFO: Cleaning up generated dataset...")
    try:
        os.remove(full_prepped_dataset_path)
    except FileNotFoundError:
        pass
    subprocess.run([
        "ls"
    ])
    subprocess.run([
        "openai", "-v"
    ])
    subprocess.run([
        "ls"
    ], shell=True)
    subprocess.run([
        "cmd", "/c", "ls", "~/"
    ])
    subprocess.run([
        "cmd", "/c", "ls", "C:\\Users\\adib\\AppData\\Local"
    ])
    subprocess.run([
        "cmd", "/c", "ls", files_path
    ])
    subprocess.run([
        "cmd", "/c", "openai", "tools", "fine_tunes.prepare_data",
        "-f", full_dataset_path,
        "-q"
    ])
    if os.path.isfile(full_prepped_dataset_path):
        get_lines(full_prepped_dataset_path, max_entry_count, reduce_mode)
    else:
        get_lines(full_dataset_path, max_entry_count, reduce_mode)

    # Train customized openAI model
    if base_model in ["davinci", "curie", "babbage", "ada"]:
        print("INFO: Training customized openAI model...")
        print("INFO: This may take a few minutes to hours depending on the size of the dataset and the selected base model")
        if os.path.isfile(full_prepped_dataset_path):
            subprocess.run([
                "openai", "api", "fine_tunes.create",
                "-t", full_prepped_dataset_path,
                "-m", base_model,
                "--suffix", user_id,
                "--no_check_if_files_exist"
            ])
        else:
            subprocess.run([
                "openai", "api", "fine_tunes.create",
                "-t", full_dataset_path,
                "-m", base_model,
                "--suffix", user_id,
                "--no_check_if_files_exist"
            ])
    elif base_model == "none":
        print("INFO: No base model selected... Skipping training.")

    # Clean up generated files
    if clean:
        try:
            os.remove(full_dataset_path)
            os.remove(full_prepped_dataset_path)
        except FileNotFoundError:
            pass
