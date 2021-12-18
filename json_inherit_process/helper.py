import re


def separate_value_unit(s: str):
    r = "^((\-|\+)?\s*\d+(\.\d+)?)\s*(\S*)$"
    m = re.search(r, s)
    return float(m.group(1).replace(" ", "")), m.group(4)


def have_number(s: str):
    r = "^(\-|\+)?\s*\d+(\.\d+)?"
    m = re.search(r, s)
    return m != None


def get_paths_str(paths: list[str]) -> str:
    resutl = ""
    for path in paths:
        if len(resutl) > 0:
            resutl += "."
        resutl += path
    return resutl


def test():
    test = "324"
    assert have_number(test)
    assert separate_value_unit(test) == (324, "")


def test1():
    test = "324.34"
    assert have_number(test)
    assert separate_value_unit(test) == (324.34, "")


def test2():
    test = "-324.34 "
    assert have_number(test)
    assert separate_value_unit(test) == (-324.34, "")


def test3():
    test = "- 324.34"
    assert have_number(test)
    assert separate_value_unit(test) == (-324.34, "")


def test4():
    test = "- 324.3434"
    assert have_number(test)
    assert separate_value_unit(test) == (-324.3434, "")


def test5():
    test = "- 324.3434df"
    assert have_number(test)
    assert separate_value_unit(test) == (-324.3434, "df")


def test6():
    test = "- 324.3434 df"
    assert have_number(test)
    assert separate_value_unit(test) == (-324.3434, "df")


def test7():
    test = "sfd"
    assert not have_number(test)


if __name__ == "__main__":
    test()
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
