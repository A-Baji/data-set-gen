from appdirs import user_data_dir
from re import sub
from json import load, dumps
from datetime import timedelta
from dateutil import parser
from os import path


def parse_logs(file: str, user: str, thought_time=10):
    files_path = user_data_dir(appname="discordai")
    dataset = open(
        path.join(files_path, f"{file.split(files_path+path.sep)[1].split('_')[0]}_{user}_data_set.jsonl"), 'w')
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
                        if len(thought.split(" ")) > 3:  # If the thought has more than three words
                            dataset.write(
                                dumps(
                                    {'prompt': '', 'completion': f'{thought}'
                                     if thought[-1] == '.' else f'{thought}.'}) + "\n")
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
