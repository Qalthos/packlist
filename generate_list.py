#!/usr/bin/env python
import sys
from pathlib import Path

import yaml
from docutils.core import publish_string

Container = dict[str, "Pocket"]
Pocket = list[str | Container]


def print_pocket(pocket: Pocket, /, prefix: str = "") -> str:
    lines = []
    for item in pocket:
        if isinstance(item, dict):
            for name, subpocket in item.items():
                lines.append(f"{prefix}* {name}:\n")
                lines.append(print_pocket(subpocket, prefix=prefix + "  "))
        else:
            lines.append(f"{prefix}* ☐ {item}")
    return "\n".join(lines)


def print_container(container: Container) -> str:
    lines = []
    for name, pocket in container.items():
        if pocket:
            lines.append(f"{name}\n{'-' * len(name)}\n")
            lines.append(print_pocket(pocket))
            lines.append("")

    return "\n".join(lines)


def parse_yaml(config: Path) -> str:
    with config.open("r") as yaml_file:
        items: dict[str, Container | Pocket] = yaml.safe_load(yaml_file)

    lines = []
    for name, container in items.items():
        lines.append(f"{name}\n{'=' * len(name)}\n")
        if isinstance(container, dict):
            lines.append(print_container(container))
        else:
            lines.append(print_pocket(container))
            lines.append("")

    return "\n".join(lines)


def main() -> None:
    config = Path(sys.argv[1])
    if not config.exists():
        print(f"Could not find source file {config}")
        sys.exit(1)

    rst_str = parse_yaml(config)

    settings = dict(
        title=config.name, stylesheet_path="style.css", embed_stylesheet=False
    )

    html_data = publish_string(
        rst_str, writer_name="html5", settings_overrides=settings
    )

    with Path("packlist.html").open("wb") as output_file:
        output_file.write(html_data)


if __name__ == "__main__":
    main()
