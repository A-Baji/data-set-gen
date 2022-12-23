import json
import datetime
import sys
import re


def gen_data_set(file, user, thought_time=10000):
    dataset = open(f'{file}_{user}_data_set.jsonl', 'w')
    user_dat = user.split('#')
    with open(file, 'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
        messages = [msg for msg in data['messages']
                    if msg['author']['name'] == user_dat[0] and msg['author']['discriminator'] == user_dat[1]]
        thought = ''
        for i, msg in enumerate(messages):
            msg['content'] = re.sub(
                r'\b(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~|!:,.;]+[-A-Za-z0-9+&@#/%=~_|?.]+[-A-Za-z0-9+&@#/%=~_|?]', '', msg['content'])
            if msg['content']:
                if i == 0:
                    thought = msg['content']
                if i > 0:
                    prev_timestamp = datetime.datetime.fromisoformat(
                        messages[i-1]['timestamp'])
                    curr_timestamp = datetime.datetime.fromisoformat(
                        msg['timestamp'])
                    differentiation = (curr_timestamp - prev_timestamp) / \
                        datetime.timedelta(milliseconds=1)
                    if differentiation > thought_time:  # If time between messages exceed `thought_time` milliseconds
                        if len(thought.split(" ")) > 3:  # If the thought has more than three words
                            dataset.write(json.dumps(
                                {'prompt': '', 'completion': thought if thought[-1] == '.' else thought + '.'}) + "\n")
                        thought = msg['content']
                    else:
                        thought += f" {msg['content']}"
                    # If it is the last message and the thought has more than three words
                    if i == len(messages)-1 and len(thought.split(" ")) > 3:
                        dataset.write(json.dumps(
                            {'prompt': '', 'completion': thought if thought[-1] == '.' else thought + '.'}) + "\n")
    dataset.close()


if __name__ == '__main__':
    gen_data_set(sys.argv[1], sys.argv[2])
