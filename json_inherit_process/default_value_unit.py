data = {
    "body_part": {
        "encumbrance_limit": 100,
        "smash_efficiency": 0.5
    },
    "bionic": {
        "act_cost": "0 kj",
        "deact_cost": "0 kj",
        "react_cost": "0 kj",
        "trigger_cost": "0 kj",
        "time": "0 t",
        "weight_capacity_bonus": "0 g",
        "weight_capacity_modifier": 1,
        "capacity": "1 kj",
        "coverage_power_gen_penalty": 1
    },
    "material": {
        "wind_resist": 99,
        "specific_heat_liquid": 4.168,
        "specific_heat_solid": 2.108,
        "latent_heat": 334,
        "freezing_point": "0 c"
    },
    "monster": {
        "mountable_weight_ratio": 0.2,
        "grab_strength": 1,
        "tracking_distance": 3,
        "bleed_rate": 100,
        "path_settings": {
            "allow_climb_stairs": True
        }
    },
    "monster_attack": {
        "move_cost": 100,
        "attack_chance": 100,
        "attack_upper": True,
        "range": 1
    },
    "mutation_type": {
        "iv_sleep_dur": "0 t"
    },
    "recipe": {
        "scent_modifier": 1,
        "scent_intensity": 500,
        "healthy_rate": 1
    },
    "vehicle_part": {
        "damage_modifier": 100,
        "cargo_weight_modifier": 100
    },
    "generic": {
        "weight": "0 g",
        "volume": "0 l",
        "integral_volume": "0 l",
        "integral_weight": "0 g",
        "insulation": 1,
        "price": "0 usd",
        "price_postapoc": "0 usd",
        "seed_data": {
            "seeds": True,
            "fruit_div": 1
        }
    },
    "armor": {
        "weight_capacity_modifier": 1
    },
    "comestible": {
        "monotony_penalty": 2,
        "freezing_point": "32 f"
    },
    "gun": {
        "blackpowder_tolerance": 8,
        "consume_chance": 10000,
        "consume_divisor": 1
    },
    "furniture": {
        "bonus_fire_warmth_feet": 300,
        "boltcut": {
            "duration": "1 seconds"
        },
        "oxytorch": {
            "duration": "1 seconds"
        },
        "prying": {
            "duration": "1 seconds"
        },
        "hacksaw": {
            "duration": "1 seconds"
        }
    },
    "terrain": {
        "bonus_fire_warmth_feet": 300,
        "boltcut": {
            "duration": "1 seconds"
        },
        "oxytorch": {
            "duration": "1 seconds"
        },
        "prying": {
            "duration": "1 seconds"
        },
        "hacksaw": {
            "duration": "1 seconds"
        }
    },
    "scenario": {
        "custom_initial_date": {
            "hour": 8,
            "year": 1
        }
    },
    "overlay_order": {
        "order": 9999
    },
    "field_type": {
        "move_cost": 100
    }
}


def get_default_value_unit(type: str, paths: list[str]):
    paths = [type]+paths
    return __get_default_value_unit_part(paths, data)


def __get_default_value_unit_part(paths: list[str], current_data):
    if type(current_data) is dict:
        if len(paths) == 0:
            return None
        key = paths.pop(0)
        if key in current_data:
            return __get_default_value_unit_part(paths, current_data[key])
        else:
            return None
    else:
        if len(paths) == 0:
            return current_data
        else:
            return None
