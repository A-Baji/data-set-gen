import json
import datetime
import sys


def gen_data_set(file, user, thought_time=10000):
    dataset = open(f'{user}_data_set.jsonl', 'w')
    user_dat = user.split('#')
    with open(file, 'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
        messages = [msg for msg in data['messages']
                    if msg['author']['name'] == user_dat[0] and msg['author']['discriminator'] == user_dat[1]]
        thought = ''
        for i, msg in enumerate(messages):
            if msg['content']:
                if i == 0:
                    thought += msg['content']
                if i > 0:
                    prev_timestamp = datetime.datetime.fromisoformat(
                        messages[i-1]['timestamp'])
                    curr_timestamp = datetime.datetime.fromisoformat(
                        msg['timestamp'])
                    differentiation = (curr_timestamp - prev_timestamp) / \
                        datetime.timedelta(milliseconds=1)
                    if differentiation > thought_time:
                        dataset.write(json.dumps(
                            {'prompt': '', 'completion': thought}) + "\n")
                        thought = msg['content']
                    else:
                        thought += f" {msg['content']}"
    dataset.close()


if __name__ == '__main__':
    gen_data_set(sys.argv[1], sys.argv[2])
