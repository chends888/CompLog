with open('test.vbs', 'r', encoding='utf-8') as infile:
    lines = ''
    for line in infile:
        lines += line
print(len(lines))