from typing import List, Any


def stringify_dictionary(data: dict, names: List[str]) -> dict:
    for name in data:
        if name in names:
            data[name] = str(data[name])
    return data


def stringify_list(data: List[Any]) -> List[str]:
    data = [str(item) for item in data]
    return data