from math import ceil
from appdirs import user_data_dir
from re import sub
from json import load, dumps
from datetime import timedelta
from dateutil import parser
from string import punctuation
from os import path
import pathlib


def parse_logs(
    file: str,
    channel: str,
    user: str,
    model: str,
    thought_time=10,
    thought_max: int = None,
    thought_min=4,
):

    def validate_thought(thought: str) -> bool:
        """
        If the thought's word count is within `thought_min` and `thought_max`,
            return True
        """
        word_count = len(thought.split(" ")) - 1
        if word_count >= thought_min and thought_max >= word_count:
            return True

    def clean_message(msg: dict) -> dict:
        """
        Remove URLs from a message and,
            return the message
        """
        msg["content"] = sub(
            r"\bhttps?://\S+|\bftp://\S+|\bfile://\S+", "", msg["content"]
        )
        return msg

    def build_thought(thought: str, msg: dict) -> str:
        """
        Add a message to a thought and,
            return the thought
        """
        content = msg["content"].strip()  # Remove leading/trailing spaces
        if content:
            thought += f" {content}"
        return thought

    def build_json(thought: str) -> str:
        """
        Create a new dataset JSON entry string and,
            return the JSON entry string
        """
        if thought[-1] not in punctuation:
            thought += "."
        if model == "gpt3":
            return (
                dumps(
                    {
                        "messages": [
                            {
                                "role": "system",
                                "content": f"{username} is a conversational chatbot that imitates the user {username}.",
                            },
                            {"role": "user", "content": f"{username} says:"},
                            {"role": "assistant", "content": thought},
                        ]
                    }
                )
                + "\n"
            )
        else:
            return dumps({"prompt": f"{username} says:", "completion": thought}) + "\n"

    def add_to_dataset(thought: str):
        """
        Validate a thought, create a dataset JSON entry, and then add it to the dataset
        """
        if validate_thought(thought):
            dataset.write(build_json(thought))

    files_path = pathlib.Path(user_data_dir(appname="discordai"))
    dataset = open(files_path / f"{channel[:4]}_{user}_data_set.jsonl", "w")
    thought_max = 999999 if not thought_max else thought_max
    if "#" in user:
        username, user_id = user.split("#")
    else:
        username, user_id = user, None
    with open(file, "r", encoding="utf-8") as data_file:
        data = load(data_file)
        messages = [
            clean_message(msg)
            for msg in data["messages"]
            if msg["author"].get("name") == username
            and (user_id is None or msg["author"].get("discriminator") == user_id)
        ]
        thought = build_thought("", messages[0])
        for i, msg in enumerate(messages[1::]):
            if msg["content"]:
                prev_timestamp = parser.parse(messages[i - 1]["timestamp"])
                curr_timestamp = parser.parse(msg["timestamp"])
                differentiation = (curr_timestamp - prev_timestamp) / timedelta(
                    milliseconds=1
                )
                if differentiation > thought_time * 1000:
                    add_to_dataset(thought)
                    thought = build_thought("", msg)
                else:
                    thought = build_thought(thought, msg)
        add_to_dataset(thought)
    dataset.close()
    if path.getsize(files_path / f"{channel[:4]}_{user}_data_set.jsonl") == 0:
        print(
            "WARNING: The resulting dataset is empty. Please double check your parameters."
        )


def get_lines(file_name: str, N=1000, offset=0, select_mode="start", reverse=False):
    with open(file_name, "r") as f:
        lines = f.readlines()
    f.close()

    num_lines = len(lines)
    if N > num_lines:
        return

    if select_mode == "sequential":
        step = 1
    else:
        step = ceil(num_lines // N)

    print(reverse)
    if reverse:
        lines = lines[::-1]

    offset -= 1
    selected_lines = lines[offset:][::step][: offset + N]
    if len(selected_lines) > N:
        selected_lines = selected_lines[:N]

    with open(file_name, "w") as f:
        f.writelines(selected_lines)
    f.close()
