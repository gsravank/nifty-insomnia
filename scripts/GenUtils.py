def read_lines(filename):
    lines = list()
    with open(filename, 'r') as f:
        for line in f.readlines():
            if len(line.strip()):
                lines.append(line.strip())
    return lines


def write_lines(lines, filename):
    with open(filename, 'w') as f:
        f.write('\n'.join(lines))
