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
        "s": 1,
        "seconds": 1,
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
    },
    {
        "cent": 0.01,
        "usd": 1,
        "kusd": 1000
    }
]


def convert_SI(val: float, unit_in: str, unit_out: str):
    unit_in = unit_in.lower()
    unit_out = unit_out.lower()
    if unit_in == "c" and unit_out == "f":
        return convert_f(unit_in)
    elif unit_in == "f" and unit_out == "c":
        return convert_c(unit_in)
    SI_unit = None
    for unit in SI_list:
        if unit_in in unit and unit_out in unit:
            SI_unit = unit
            break
    if SI_unit == None:
        raise Exception(f"No find SI_unit:{unit_in},{unit_out}")
    return val*SI_unit[unit_in]/SI_unit[unit_out]


def convert_f(c: float) -> float:
    return c * 1.8 + 32


def convert_c(f: float) -> float:
    return (f-32)/1.8


def test():
    assert convert_SI(100, "cm", "m") == 1
    assert convert_SI(100, "m", "t") == 6000


if __name__ == "__main__":
    test()
