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

class Config():
    """manage interaction with mdk config file"""
    def __init__(self):
        config_dir_path = Path.home()/".config/mdk"
        if not config_dir_path.exists():
            config_dir_path.mkdir(parents=True)
            os.chown(
                config_dir_path,
                os.geteuid(),
                os.getgid())

        if not self.shared_path_host.exists():
            self.shared_path_host.mkdir(parents=True)
            os.chown(
                self.shared_path_host,
                os.geteuid(),
                os.getgid())

    def __getattr__(self, name):
        """get val of key from persistent storage"""
        data_store = shelve.open(str(Path.home()/".config/mdk/config.mdk"))
        config_defaults = {
            "autogen_active": True,
            "autogen_dir": ".autogen",
            "autogen_name": "autogen",
            "service_name": None,
            "service_dir": None,
            "shared_path_host": Path.home()/"mdkshared",
            "shared_path_target": "/home/matic/mdkshared",
            "overrides_dir": Path.home()/".config/mdk/"}

        # when pulling value, use data store > default > None
        val = data_store.get(
            name,
            config_defaults.get(
                name,
                None))

        data_store.close()
        return val

    def __setattr__(self, name, value):
        """set key:val in persistent storage"""
        data_store = shelve.open(str(Path.home()/".config/mdk/config.mdk"))
        if isinstance(value, str) and value.strip().lower() in ["true", "false"]:
            value = (value.strip().lower() == 'true')
        data_store[name] = value
        data_store.close()


class Log():
    """unified mdk console logging"""
    @staticmethod
    def __call__(message):
        """generic message formatting"""
        click.echo(message)

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
    if detach is True:
        return subprocess.getoutput(" ".join(cmd_builder))
    return subprocess.call(cmd_builder)


def docker_compose(args: List[str], detach=False):
    """$ docker-compose [args], from directory of current service"""
    config = Config()
    cmd_builder = ["docker-compose"]
    if config.autogen_active is True and autogen_config() is not None:
        print('adding')
        cmd_builder.extend(["-f", "docker-compose.yaml"])
        cmd_builder.extend(["-f", "{}/{}.yaml".format(config.autogen_dir, config.autogen_name)])

    cmd_builder.extend(args)
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
            history_file = "{}/.{}.bash_history".format(config.shared_path_target, container_name)
        else:
            container_name = "container_name not set for {}".format(service)
            history_file = "{}/.bash_history".format(config.shared_path_target)

        conf_builder["services"][service] = {
            "environment": {
                "DOCKER_CONTAINER_NAME": container_name,
                "DOCKER_CONTAINER_ROOT": '~/' + str(config.service_dir.relative_to(Path.home())),
                "HISTFILE": history_file,
                "HOST_UID": "${UID:-1000}"},
            "volumes": [
                "$HOME/{}:{}".format(
                    config.shared_path_host.relative_to(Path.home()), config.shared_path_target)]}

    for raw in [x for x in config.overrides_dir.iterdir() if x.suffix in [".yml", ".yaml"]]:
        overrides = parse_yaml(raw)
        if overrides is None or \
           ("version" in overrides and overrides["version"] != conf_builder["version"]):
            continue
        for service, service_conf in overrides.pop("services", {}).items():
            if service in conf_builder["services"]:
                conf_builder["services"][service] = merge_dicts(
                    service_conf,
                    conf_builder["services"][service])
        conf_builder = merge_dicts(overrides, conf_builder)

    SafeDumper.add_representer(
        type(None),
        lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', ''))
    autogen_path = config.service_dir/config.autogen_dir
    autogen_path.mkdir(exist_ok=True)
    compose_path = autogen_path/("{}.yaml".format(config.autogen_name))
    compose_stream = compose_path.open("w")
    yaml.dump(conf_builder, compose_stream, Dumper=SafeDumper)
    return conf_builder
