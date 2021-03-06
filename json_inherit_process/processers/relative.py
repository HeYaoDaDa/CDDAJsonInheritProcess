from os import path
from ..helper import have_number, separate_value_unit
from ..unit_helper import convert_SI
from ..default_value_unit import get_default_value_unit


def process_relative(processed_json_object: dict, inherit_templet: dict):
    if "relative" in inherit_templet:
        process_relative_unit(
            inherit_templet["relative"],
            processed_json_object,
            [],
            inherit_templet["type"],
            processed_json_object["type"]
        )
        del inherit_templet["relative"]


def __get_default_unit(jsonType: str, paths: list[str]) -> str:
    default_data = get_default_value_unit(
        jsonType, paths
    )
    if (type(default_data) is str) and have_number(default_data):
        default_value, default_unit = separate_value_unit(
            default_data)
        return(default_unit)
    else:
        raise Exception(
            f"not find jsonType {jsonType}, field {paths} default value")


def __process_relative_unit_unit(key: str, value: str, super: dict, paths: list[str], sub_type: str, super_type: str):
    if key in super:
        if type(super[key]) is dict:
            process_relative_unit(
                value, super[key], paths, sub_type, super_type)
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
                    suf = __get_default_unit(super_type, paths)
                if type(value) is str:
                    num1, suf1 = separate_value_unit(value)
                else:
                    num1 = value
                    suf1 = __get_default_unit(sub_type, paths)
                if suf == "":
                    suf = suf1
                if suf1 == "":
                    suf1 = suf
                if suf != suf1:
                    print(
                        f"need convert unit, val is {num1}, unit is {suf1}, to unit is {suf}")
                    num1 = convert_SI(num1, suf1, suf)
                    print(
                        f"convert result is {num1}, unit is {suf}")
                super[key] = str(num + num1) + " " + suf
        else:
            super[key] += value
    else:
        default_data = get_default_value_unit(
            super_type, paths
        )
        if not default_data == None:
            super[key] = default_data
            __process_relative_unit_unit(
                key, value, super, paths, sub_type, super_type
            )
        else:
            super[key] = value


def process_relative_unit(sub: dict, super: dict, paths: list[str], sub_type: str, super_type: str):
    # fuck to_hit
    if type(sub) is int:
        value = sub
        sub = dict()
        for key in super.keys():
            sub[key] = value
    for key, value in sub.items():
        paths.append(key)
        __process_relative_unit_unit(
            key, value, super, paths, sub_type, super_type
        )
        paths.pop()


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
