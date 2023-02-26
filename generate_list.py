#!/usr/bin/env python
from pathlib import Path

import yaml

Container = dict[str, "Pocket"]
Pocket = list[str | Container]


def print_pocket(pocket: Pocket, /, prefix: str = ""):
    for item in pocket:
        if isinstance(item, dict):
            for name, subpocket in item.items():
                print(f"{prefix}* {name}:\n")
                print_pocket(subpocket, prefix=prefix + "  ")
        else:
            print(f"{prefix}* ☐ {item}")


def print_container(container: Container):
    for name, pocket in container.items():
        if pocket:
            print(f"{name}\n{'-' * len(name)}\n")
            print_pocket(pocket)
            print()


def main():
    config = Path("items.yaml")
    with open(config, "r") as yaml_file:
        items: dict[str, Container | Pocket] = yaml.safe_load(yaml_file)

    for name, container in items.items():
        print(f"{name}\n{'=' * len(name)}\n")
        if isinstance(container, dict):
            print_container(container)
        else:
            print_pocket(container)
            print()


if __name__ == "__main__":
    main()
