import os
import sys
import subprocess

from gen_dataset import parse_logs

# Usage:
# python create_model.py <channel id> <"discord user#id"> <max dataset entry count=1000>
#                        <reduce_mode:first|last|middle|even=even> <ada|babbage|curie|davinci|none <- skips model building>
#                        <clean|dirty <- keeps generated files> <discord bot token> <openai api key>

os.environ["OPENAI_API_KEY"] = sys.argv[8]

# Download logs
if not os.path.isfile(f"{sys.argv[1]}_{sys.argv[2]}_logs.json"):
    print("INFO: Exporting chat logs using DiscordChatExporter...")
    print("INFO: This may take a few minutes to hours depending on the message count of the channel")
    print("INFO: Progress will NOT be saved if cancelled")
    print("---------------DiscordChatExporter---------------")
    subprocess.run([
        "./DiscordChatExporter/DiscordChatExporter.Cli.exe",
        "export",
        "-c", sys.argv[1],
        "-t", sys.argv[7],
        "-o", f"{sys.argv[1]}_{sys.argv[2]}_logs.json",
        "-f", "Json",
        "--filter", f"from:'{sys.argv[2]}'"
    ])
    print("---------------DiscordChatExporter---------------")
else:
    print("INFO: Chat logs detected locally... Skipping download.")

# Parse logs
if not os.path.isfile(f"{sys.argv[1]}_{sys.argv[2]}_data_set.jsonl"):
    print("INFO: Parsing chat logs into a openAI compatible dataset...")
    parse_logs(f"{sys.argv[1]}_{sys.argv[2]}_logs.json", sys.argv[2])
    try:
        os.remove(f"{sys.argv[1]}_{sys.argv[2]}_data_set_prepared.jsonl")
    except FileNotFoundError:
        pass
else:
    print("INFO: Dataset detected locally... Skipping parsing.")

# Prepare and reduce dataset
if not os.path.isfile(f"{sys.argv[1]}_{sys.argv[2]}_data_set_prepared.jsonl"):
    print("INFO: Cleaning up generated dataset...")
    subprocess.run([
        "openai", "tools", "fine_tunes.prepare_data",
        "-f", f"{sys.argv[1]}_{sys.argv[2]}_data_set.jsonl",
        "-q"
    ])
    if os.path.isfile(f"{sys.argv[1]}_{sys.argv[2]}_data_set_prepared.jsonl"):
        subprocess.run([
            "python3.11",
            "reduce_dataset.py",
            f"{sys.argv[1]}_{sys.argv[2]}_data_set_prepared.jsonl",
            sys.argv[3],
            sys.argv[4]
        ])
    else:
        subprocess.run([
            "python3.11",
            "reduce_dataset.py",
            f"{sys.argv[1]}_{sys.argv[2]}_data_set.jsonl",
            sys.argv[3],
            sys.argv[4]
        ])

# Train customized openAI model
if sys.argv[5] in ["davinci", "curie", "babbage", "ada"]:
    print("INFO: Training customized openAI model...")
    print("INFO: This may take a few minutes to hours depending on the size of the dataset and the selected base model")
    if os.path.isfile(f"{sys.argv[1]}_{sys.argv[2]}_data_set_prepared.jsonl"):
        subprocess.run([
            "openai", "api", "fine_tunes.create",
            "-t", f"{sys.argv[1]}_{sys.argv[2]}_data_set_prepared.jsonl",
            "-m", sys.argv[5],
            "--suffix", sys.argv[2]
        ])
    else:
        subprocess.run([
            "openai", "api", "fine_tunes.create",
            "-t", f"{sys.argv[1]}_{sys.argv[2]}_data_set.jsonl",
            "-m", sys.argv[5],
            "--suffix", sys.argv[2]
        ])
else:
    print("INFO: No base model selected... Skipping training.")

# Cleaning up generated files
if sys.argv[6] == "clean":
    try:
        os.remove(f"{sys.argv[1]}_{sys.argv[2]}_data_set.jsonl")
        os.remove(f"{sys.argv[1]}_{sys.argv[2]}_data_set_prepared.jsonl")
    except FileNotFoundError:
        pass
