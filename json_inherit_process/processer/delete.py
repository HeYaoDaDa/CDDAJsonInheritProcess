def process_delete(processed_json_object: dict, inherit_templet: dict):
    if "delete" in inherit_templet:
        for key, value in inherit_templet["delete"].items():
            if key in processed_json_object:
                if not type(value) is list:
                    value = [value]
                if not type(processed_json_object[key]) is list:
                    processed_json_object[key] = [processed_json_object[key]]
                for i in range(len(processed_json_object[key]))[::-1]:
                    if processed_json_object[key][i] in value:
                        del processed_json_object[key][i]
        del inherit_templet["delete"]


def test():
    process_json_object = {"id": "test_object",
                           "flags": ["flag1", "flag2", "flag3", "flag4"]}
    inherit_templet = {"id": "test", "delete": {"flags": ["flag3", "flag4"]}}

    process_delete(process_json_object, inherit_templet)

    assert process_json_object == {
        'id': 'test_object', 'flags': ['flag1', 'flag2']}


def test1():
    process_json_object = {
        'id': 'test_object', 'flags': ['flag1', 'flag4']}
    inherit_templet = {"id": "test", "delete": {"flags": "flag4"}}

    process_delete(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object",
                                   "flags": ["flag1"]}


def test2():
    process_json_object = {'id': 'test_object', 'flags': 'flag4'}
    inherit_templet = {"id": "test", "delete": {"flags": "flag4"}}

    process_delete(process_json_object, inherit_templet)

    assert process_json_object == {"id": "test_object", 'flags': []}


if __name__ == "__main__":
    test()
    test1()
    test2()
