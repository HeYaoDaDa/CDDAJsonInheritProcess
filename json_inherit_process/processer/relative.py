from ..helper import have_number, separate_value_unit


def process_relative(processed_json_object: dict, inherit_templet: dict):
    process_relative_unit(inherit_templet["relative"], processed_json_object)
    del inherit_templet["relative"]


def process_relative_unit(sub: dict, super: dict):
    for key, value in sub.items():
        if key in super:
            if type(super[key]) is dict:
                process_relative_unit(value, super[key])
            elif type(super[key]) is str or type(value) is str:
                if (type(super[key]) is str and have_number(super[key])) or (type(value) is str and have_number(value)):
                    num = 0
                    num1 = 0
                    suf = ""
                    suf1 = ""
                    if type(super[key]) is str:
                        num, suf = separate_value_unit(super[key])
                    else:
                        num = super[key]
                    if type(value) is str:
                        num1, suf1 = separate_value_unit(value)
                    else:
                        num1 = value
                    if suf == "":
                        suf = suf1
                    if suf1 == "":
                        suf1 = suf
                    if suf != suf1:
                        print("suf:{}  suf1:{}".format(suf, suf1))
                    super[key] = str(num + num1) + " " + suf
            else:
                super[key] += value
        else:
            super[key] = value


def test():
    process_json_object = {"id": "test_object",
                           "test": 10}
    inherit_templet = {"id": "test", "relative": {"test": 10}}

    process_relative(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": 20}


def test1():
    process_json_object = {"id": "test_object",
                           "test": 10}
    inherit_templet = {"id": "test", "relative": {"test": "10ml"}}

    process_relative(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "20.0 ml"}


def test2():
    process_json_object = {"id": "test_object",
                           "test": "10ml"}
    inherit_templet = {"id": "test", "relative": {"test": 10}}

    process_relative(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "20.0 ml"}


def test3():
    process_json_object = {"id": "test_object",
                           "test": 10}
    inherit_templet = {"id": "test", "relative": {"test": "10 ml"}}

    process_relative(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "20.0 ml"}


def test4():
    process_json_object = {"id": "test_object",
                           "test": "10 ml"}
    inherit_templet = {"id": "test", "relative": {"test": 10}}

    process_relative(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "20.0 ml"}


def test5():
    process_json_object = {"id": "test_object",
                           "test": "10ml"}
    inherit_templet = {"id": "test", "relative": {"test": "10ml"}}

    process_relative(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "20.0 ml"}


def test6():
    process_json_object = {"id": "test_object",
                           "test": "10 ml"}
    inherit_templet = {"id": "test", "relative": {"test": "10ml"}}

    process_relative(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "20.0 ml"}


def test7():
    process_json_object = {"id": "test_object",
                           "test": "10ml"}
    inherit_templet = {"id": "test", "relative": {"test": "10 ml"}}

    process_relative(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "20.0 ml"}


def test7():
    process_json_object = {"id": "test_object",
                           "test": 30}
    inherit_templet = {"id": "test", "relative": {"test": -10}}

    process_relative(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": 20}


def test8():
    process_json_object = {"id": "test_object",
                           "test": 30}
    inherit_templet = {"id": "test", "relative": {"test": -40}}

    process_relative(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": -10}


def test9():
    process_json_object = {"id": "test_object",
                           "test": 30}
    inherit_templet = {"id": "test", "relative": {"test": "-10 ml"}}

    process_relative(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "20.0 ml"}


def test10():
    process_json_object = {"id": "test_object",
                           "test": 30}
    inherit_templet = {"id": "test", "relative": {"test": "-40 ml"}}

    process_relative(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "-10.0 ml"}


if __name__ == "__main__":
    test()
    test1()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()
