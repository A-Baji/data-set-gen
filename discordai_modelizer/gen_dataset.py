from appdirs import user_data_dir
from re import sub
from json import load, dumps
from datetime import timedelta
from dateutil import parser
from string import punctuation
import pathlib

def parse_logs(file: str, channel:str, user: str, thought_time=10, thought_max: int = None, thought_min=4):
    files_path = pathlib.Path(user_data_dir(appname="discordai"))
    dataset = open(files_path / f"{channel}_{user}_data_set.jsonl", 'w')
    thought_max = 999999 if not thought_max else thought_max
    with open(file, 'r', encoding='utf-8') as data_file:
        data = load(data_file)
        messages = [msg for msg in data['messages']
                    if f"{msg['author']['name']}#{msg['author']['discriminator']}" == user]
        thought = ''
        for i, msg in enumerate(messages):
            msg['content'] = sub(
                r'\b(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~|!:,.;]+[-A-Za-z0-9+&@#/%=~_|?.]+[-A-Za-z0-9+&@#/%=~_|?]',
                '', msg['content'])
            if msg['content']:
                if i == 0:
                    thought = msg['content'] if msg['content'][
                        0] == ' ' else f" {msg['content']}"
                if i > 0:
                    prev_timestamp = parser.parse(
                        messages[i-1]['timestamp'])
                    curr_timestamp = parser.parse(
                        msg['timestamp'])
                    differentiation = (curr_timestamp - prev_timestamp) / \
                        timedelta(milliseconds=1)
                    if differentiation > thought_time*1000:  # If time between messages exceed `thought_time` milliseconds
                        if len(thought.split(" "))-1 >= thought_min and thought_max >= len(thought.split(" "))-1:  # If the thought size is within `thought_min` and `thought_max`
                            dataset.write(
                                dumps(
                                    {'prompt': '', 'completion': f'{thought}'
                                     if thought[-1] in punctuation else f'{thought}.'}) + "\n")
                        thought = msg['content'] if msg['content'][
                            0] == ' ' else f" {msg['content']}"
                    else:
                        thought += f" {msg['content']}"
                    # If it is the last message and the thought has more than three words
                    if i == len(messages)-1 and len(thought.split(" ")) > 3:
                        dataset.write(
                            dumps(
                                {'prompt': '', 'completion': f'{thought}'
                                 if thought[-1] == '.' else f'{thought}.'}) + "\n")
    dataset.close()


def get_lines(file_name, N, method):
    with open(file_name, "r") as f:
        lines = f.readlines()
    num_lines = len(lines)

    if N > num_lines:
        return

    if method == 'first':
        selected_lines = lines[:N]
    elif method == 'last':
        selected_lines = lines[-N:]
    elif method == 'middle':
        start = num_lines // 2 - N // 2
        end = start + N
        selected_lines = lines[start:end]
    else:
        if method != 'even':
            print("Invalid reduce method... Defaulting to even mode.")
        interval = num_lines // N
        selected_lines = []
        for i in range(N):
            selected_lines.append(lines[i * interval])
        start = num_lines
        while len(selected_lines) < N:
            end = start + N - len(selected_lines)
            selected_lines += lines[:end]
            start = 1

    with open(file_name, "w") as f:
        f.writelines(selected_lines)
