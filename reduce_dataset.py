import sys


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
        step = 5
        start = 0
        selected_lines = lines[start::step][:N]
        while len(selected_lines) < N:
            middle = num_lines // 2
            start = middle - step // 2
            if start in selected_lines:
                start += 1
            selected_lines += lines[start::step]
            selected_lines = list(set(selected_lines))
        while len(selected_lines) < N:
            middle = num_lines // 2
            start = middle - step // 2
            if start in selected_lines:
                start += 1
            selected_lines += lines[start-step:start+step+1:step]
            selected_lines = list(set(selected_lines))
        selected_lines = selected_lines[:N]

    with open(file_name, "w") as f:
        # Write the selected lines to the file
        f.writelines(selected_lines)


if __name__ == '__main__':
    get_lines(sys.argv[1], int(sys.argv[2]), sys.argv[3])
