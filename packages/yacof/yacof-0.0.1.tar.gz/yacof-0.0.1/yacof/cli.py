from pathlib import Path

from typing import List, NamedTuple

import configparser


class ConfigDumpSettings(NamedTuple):
    yaml_path: str
    conf_module: str
    conf_name: str


def load_setup_cfg(setup_cfg_path: str) -> List[ConfigDumpSettings]:
    parser = configparser.ConfigParser()
    parser.read(setup_cfg_path)
    settings = []
    for yaml_path in parser["yacof"]:
        module, name = parser["yacof"][yaml_path].split(":")
        settings.append(ConfigDumpSettings(yaml_path, module, name))
    return settings


def main():
    setup_cfg = "setup.cfg"
    if Path(setup_cfg).exists():
        dump_settings = load_setup_cfg(setup_cfg)
    else:
        print("No setup.cfg found")
        return 1

    for settings in dump_settings:
        import importlib

        module = importlib.import_module(settings.conf_module)
        for attr in dir(module):
            if attr == settings.conf_name:
                conf_class = getattr(module, attr)
                conf_class.export_as_yaml(settings.yaml_path)
                print(f"Saving {attr} -> {settings.yaml_path}")
