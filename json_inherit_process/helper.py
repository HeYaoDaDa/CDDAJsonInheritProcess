def separate_value_unit(s: str):
    d = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " ", "-"]
    index = -1
    for i in range(len(s))[::-1]:
        if not s[i] in d:
            index = i
    return float(s[:index]), s[index:].lstrip()


def have_number(s: str):
    d = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " ", "-"]
    for i in range(len(s))[::-1]:
        if s[i] in d:
            return True
    return False
