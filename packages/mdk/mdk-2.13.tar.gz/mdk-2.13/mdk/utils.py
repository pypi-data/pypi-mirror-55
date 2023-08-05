"""mdk utility functions & classes"""
from copy import deepcopy
import os
from pathlib import Path
import shelve
import subprocess
from typing import Any, Dict, List, Union
import click
import yaml
from yaml import SafeDumper

MDK_CONFIG_DIR: Path = Path.home()/".config/mdk"
MDK_HISTORY_DIR: Path = MDK_CONFIG_DIR/"history"
MDK_CONFIG_FILE: Path = MDK_CONFIG_DIR/".internal.mdk"

class Config():
    """manage interaction with mdk config file"""
    def __init__(self):
        for mdk_dir in [MDK_CONFIG_DIR, MDK_HISTORY_DIR]:
            if not mdk_dir.exists():
                mdk_dir.mkdir(exist_ok=True, parents=True)
                os.chown(mdk_dir, os.geteuid(), os.getgid())

    def __getattr__(self, name):
        """get val of key from persistent storage"""
        data_store = shelve.open(str(MDK_CONFIG_FILE))
        config_defaults = {
            "autogen_active": (True, bool),
            "autogen_dir": (Path(".autogen"), Path),
            "autogen_path": (Path(".autogen/mdk.yaml"), Path),
            "service_dir": (None, Path),
            "service_name": (None, str)}

        # when pulling value, use data store > default > None
        val, val_type = data_store.get(
            name,
            config_defaults.get(
                name,
                (None, type(None))))
        data_store.close()

        if val is not None:
            assert isinstance(val, val_type)
        return val

    def __setattr__(self, name, value, value_type=None):
        """set key:val in persistent storage"""
        data_store = shelve.open(str(MDK_CONFIG_FILE))
        if value_type is None:
            value_type = type(value)
        assert isinstance(value, value_type)
        if name in data_store:
            assert isinstance(value, data_store[name][1])

        data_store[name] = (value, value_type)
        data_store.close()


class Log():
    """unified mdk console logging"""
    @staticmethod
    def __call__(message):
        """generic message formatting"""
        click.echo(message)

    @staticmethod
    def command(args):
        """success formatting"""
        print_args = [arg for arg in args if isinstance(arg, str)]
        click.echo(click.style("$ " + " ".join(print_args), fg="cyan"))

    @staticmethod
    def error(context, message):
        """error formatting"""
        click.echo("{} {}:\n  {}".format(click.style("ERROR", fg="red"), context, message))

    @staticmethod
    def success(context):
        """success formatting"""
        click.echo("{}: {}".format(click.style("SUCCESS", fg="green"), context))


def docker(args: List[str], detach=False):
    """$ docker [args]"""
    cmd_builder = ["docker"] + args
    Log.command(cmd_builder)
    if detach is True:
        return subprocess.getoutput(" ".join(cmd_builder))
    return subprocess.call(cmd_builder)


def docker_compose(args: List[str], detach=False):
    """$ docker-compose [args], from directory of current service"""
    config = Config()
    cmd_builder = ["docker-compose"]
    if config.autogen_active is True and autogen_config() is not None:
        cmd_builder.extend(["-f", "docker-compose.yaml"])
        cmd_builder.extend(["-f", str(config.autogen_path)])

    cmd_builder.extend(args)
    Log.command(cmd_builder)
    if detach is True:
        return subprocess.getoutput(" ".join(args))
    return subprocess.call(cmd_builder, cwd=config.service_dir)


def merge_dicts(overrides, base):
    """recursively merge two nested dictionaries"""
    final_dict = {}
    if not isinstance(overrides, type(base)):
        return overrides
    if isinstance(overrides, list):
        return overrides + base
    if not isinstance(overrides, dict):
        return overrides
    overlapping_keys = overrides.keys() & base.keys()
    for key in overlapping_keys:
        final_dict[key] = merge_dicts(overrides[key], base[key])
    for key in overrides.keys() - overlapping_keys:
        final_dict[key] = deepcopy(overrides[key])
    for key in base.keys() - overlapping_keys:
        final_dict[key] = deepcopy(base[key])
    return final_dict


def parse_yaml(file_path: Path) -> Union[Dict[str, Any], None]:
    """yaml file reader & parser"""
    if not file_path.is_file():
        return None
    file_data = file_path.read_text()
    parsed_yaml = yaml.load(file_data, Loader=yaml.Loader) # type: Dict[str, Any]
    return parsed_yaml


def autogen_config() -> Union[Dict[str, Any], None]:
    """write an override yaml for the active service (returns a dict of written data)"""
    config = Config()
    if config.service_dir is None:
        return None

    base_conf = parse_yaml(config.service_dir/"docker-compose.yaml")
    if base_conf is None or "services" not in base_conf or "version" not in base_conf:
        return None

    conf_builder: Dict[str, Any] = {"services": {}, "version": base_conf["version"]}
    for service, service_conf in base_conf["services"].items():
        if "container_name" in service_conf:
            container_name = service_conf["container_name"]
            history_file = ".{}.bash_history".format(service_conf["container_name"])
        else:
            container_name = "container_name not set for {}".format(service)
            history_file = ".bash_history"

        conf_builder["services"][service] = {
            "environment": {
                "DOCKER_CONTAINER_NAME": container_name,
                "DOCKER_CONTAINER_ROOT": "~/" + str(config.service_dir.relative_to(Path.home())),
                "HISTFILE": "/home/matic/" + history_file,
                "HOST_UID": "${UID:-1000}"},
            "volumes": [
                "{}:/home/matic/{}".format(MDK_HISTORY_DIR/history_file, history_file)]}

    for raw in [x for x in MDK_CONFIG_DIR.iterdir() if x.suffix in [".yml", ".yaml"]]:
        overrides = parse_yaml(raw)
        if overrides is None or \
           ("version" in overrides and overrides["version"] != conf_builder["version"]):
            continue
        for service, service_conf in overrides.pop("services", {}).items():
            if service in conf_builder["services"]:
                conf_builder["services"][service] = merge_dicts(
                    service_conf,
                    conf_builder["services"][service])
            elif service == "_":
                for old_service, old_service_conf in conf_builder["services"].items():
                    conf_builder["services"][old_service] = merge_dicts(
                        service_conf,
                        old_service_conf)
        conf_builder = merge_dicts(overrides, conf_builder)

    SafeDumper.add_representer(
        type(None), lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', ''))
    config.autogen_dir.mkdir(exist_ok=True)
    compose_stream = config.autogen_path.open("w")
    yaml.dump(conf_builder, compose_stream, Dumper=SafeDumper)
    return conf_builder
