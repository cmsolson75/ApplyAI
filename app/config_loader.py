import yaml
import os


def load_config(path: str = "config.yaml") -> dict:
    """
    Load a YAML configuration file and resolve relative paths to absolute.

    Args:
        path (str, optional): Path to YAML file. Defaults to "config.yaml".

    Returns:
        dict: Configuration dictionary with normalized paths.
    """
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    base = os.path.dirname(os.path.abspath(path))
    for key, value in cfg.items():
        if isinstance(value, str):
            cfg[key] = os.path.normpath(os.path.join(base, value))
    return cfg
