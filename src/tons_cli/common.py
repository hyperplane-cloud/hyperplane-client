from configparser import ConfigParser
import logging
import os
from typing import Optional
from hyperplane.hyperplane_sdk import hyperplane_sdk


def get_path_to_conf_dir() -> str:
    base_path = "."
    if os.name == 'nt':
        base_path = os.environ.get('USERPROFILE', base_path)
    elif os.name == 'posix':
        base_path = os.environ.get('HOME', base_path)
    return os.path.join(base_path, ".tons")


def get_path_conf() -> str:
    conf_dir_path = get_path_to_conf_dir()
    conf_file_path = os.path.join(conf_dir_path, ".config")
    return conf_file_path


def read_config() -> ConfigParser:
    config = ConfigParser()
    try:
        fp = get_path_conf()
        if os.path.exists(fp):
            config.read(fp)
        else:
            logging.log("No config file")
    except Exception as e:
        logging.warn("Failed to read config")
        pass
    return config


def write_config(config : ConfigParser) -> bool:
    try:
        fp = get_path_conf()
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "wt") as f:
            config.write(f)
        return True
    except Exception as e:
        logging.error("Failed to write config parser")
        return False


def get_token() -> Optional[str]:
    token = os.getenv('HYPERPLANE_API_TOKEN')
    if token:
        return token
    conf = read_config()
    token = conf.get('DEFAULT', 'sdk_token', fallback=None)
    return token


def sdk() -> hyperplane_sdk:
    ret = hyperplane_sdk()
    token = get_token()
    ret.connect(token)
    return ret
