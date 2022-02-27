from ..helper import have_number, separate_value_unit
from ..default_value_unit import get_default_value_unit


def process_proportional(processed_json_object: dict, inherit_templet: dict):
    if "proportional" in inherit_templet:
        processed_json_object = process_proportional_unit(
            inherit_templet["proportional"],
            processed_json_object,
            [],
            inherit_templet["type"],
            processed_json_object["type"]
        )
        del inherit_templet["proportional"]


def __process_proportional_unit_unit(key: str, value, super: dict, paths: list[str], sub_type: str, super_type: str):
    if key in super:
        if type(super[key]) is str:
            if have_number(super[key]):
                num, suf = separate_value_unit(super[key])
                super[key] = str(num*value) + " " + suf
        elif type(super[key]) is dict:
            process_proportional_unit(
                value, super[key], paths, sub_type, super_type
            )
        else:
            super[key] *= value
    else:
        default_data = get_default_value_unit(
            super_type, paths
        )
        if default_data == None:
            print("-----------> not find default_data")
            print(super_type, paths)


def process_proportional_unit(sub: dict, super: dict, paths: list[str], sub_type: str, super_type: str):
    for key, value in sub.items():
        paths.append(key)
        __process_proportional_unit_unit(
            key, value, super, paths, sub_type, super_type
        )
        paths.pop()


def test():
    process_json_object = {"id": "test_object",
                           "test": 10}
    inherit_templet = {"id": "test", "proportional": {"test": 2}}

    process_proportional(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": 20}


def test1():
    process_json_object = {"id": "test_object",
                           "test": "10ml"}
    inherit_templet = {"id": "test", "proportional": {"test": 2}}

    process_proportional(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "20.0 ml"}


def test2():
    process_json_object = {"id": "test_object",
                           "test": "10 ml"}
    inherit_templet = {"id": "test", "proportional": {"test": 2}}

    process_proportional(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "20.0 ml"}


def test3():
    process_json_object = {"id": "test_object",
                           "test": "10 ml"}
    inherit_templet = {"id": "test", "proportional": {"test": 0.5}}

    process_proportional(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "5.0 ml"}


def test4():
    process_json_object = {"id": "test_object",
                           "test": "-10 ml"}
    inherit_templet = {"id": "test", "proportional": {"test": 0.5}}

    process_proportional(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "test": "-5.0 ml"}


if __name__ == "__main__":
    test()
    test1()
    test3()
    test4()
