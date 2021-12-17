SI_list = [
    {
        "g": 1,
        "kg": 1000
    },
    {
        "ml": 1,
        "l": 1000
    },
    {
        "t": 1,
        "turn": 1,
        "turns": 1,
        "m": 60,
        "minute": 60,
        "minutes": 60,
        "h": 3600,
        "hour": 3600,
        "hours": 3600,
        "d": 86400,
        "day": 86400,
        "days": 86400
    },
    {
        "mm": 0.1,
        "cm": 1,
        "dm": 10,
        "m": 100,
        "dam": 1000,
        "hm": 10000,
        "km": 100000,
    },
    {
        "mj": 0.001,
        "j": 1,
        "kj": 1000,
    }
]


def convert_SI(val: float, unit_in: str, unit_out: str):
    unit_in = unit_in.lower()
    unit_out = unit_out.lower()
    SI_unit = None
    for unit in SI_list:
        if unit_in in unit and unit_out in unit:
            SI_unit = unit
            break
    if SI_unit == None:
        raise Exception(f"No find SI_unit:{unit_in},{unit_out}")
    return val*SI_unit[unit_in]/SI_unit[unit_out]


def test():
    assert convert_SI(100, "cm", "m") == 1
    assert convert_SI(100, "m", "t") == 6000


if __name__ == "__main__":
    test()
