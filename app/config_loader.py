import yaml
import os


def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    print(cfg)
    base = os.path.dirname(os.path.abspath(path))
    for key, value in cfg.items():
        if isinstance(value, str):
            cfg[key] = os.path.normpath(os.path.join(base, value))
    return cfg
