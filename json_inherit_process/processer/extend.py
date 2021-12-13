def process_extend(processed_json_object: dict, inherit_templet: dict):
    if "extend" in inherit_templet:
        for key, value in inherit_templet["extend"].items():
            if key in processed_json_object:
                if not type(value) is list:
                    value = [value]
                if not type(processed_json_object[key]) is list:
                    processed_json_object[key] = [processed_json_object[key]]
                processed_json_object[key] += value
            else:
                processed_json_object[key] = value
        del inherit_templet["extend"]


def test():
    process_json_object = {"id": "test_object",
                           "flags": ["flag1", "flag2", "flag3"]}
    inherit_templet = {"id": "test", "extend": {"flags": ["flag4"]}}

    process_extend(process_json_object, inherit_templet)

    assert process_json_object == {
        'id': 'test_object', 'flags': ['flag1', 'flag2', 'flag3', 'flag4']}


def test1():
    process_json_object = {"id": "test_object",
                           "flags": "flag1"}
    inherit_templet = {"id": "test", "extend": {"flags": "flag4"}}

    process_extend(process_json_object, inherit_templet)

    assert process_json_object == {
        'id': 'test_object', 'flags': ['flag1', 'flag4']}


def test2():
    process_json_object = {"id": "test_object"}
    inherit_templet = {"id": "test", "extend": {"flags": "flag4"}}

    process_extend(process_json_object, inherit_templet)

    assert process_json_object == {'id': 'test_object', 'flags': 'flag4'}


if __name__ == "__main__":
    test()
    test1()
    test2()
