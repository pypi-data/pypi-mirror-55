"""mdk is a docker-compose helper"""
# pylint: disable=too-many-locals,too-many-statements,unused-argument,unused-variable
from pathlib import Path
import sys
from typing import Callable
import click
import pkg_resources
from mdk import utils
from mdk.utils import docker, docker_compose

VERSION = pkg_resources.require("mdk")[0].version

def requires_active_service(func) -> Callable:
    """decorator to gate a command by presence of active service"""
    def active_service_decorator(*args, **kwargs):
        config = utils.Config()
        if config.service_name is None or config.service_dir is None:
            utils.Log.error("executing mdk command", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)
        else:
            func(*args, **kwargs)

    return active_service_decorator


def mdk(*args, **kwargs):
    """set up and execute the mdk cli"""
    @click.group()
    @click.version_option(version=VERSION)
    @click.pass_context
    def cli(ctx, prog_name="mdk"):
        """docker/docker-compose helper and taskrunner"""

    config = utils.Config()
    log = utils.Log()
    mdk_command = cli.command

    @mdk_command(
        name="bash",
        short_help="attach a bash shell for the active, running service")
    @requires_active_service
    def mdk_bash():
        """attach a bash shell for the active, running service

        $ docker-compose exec [service] bash"""
        docker_compose(["exec", config.service_name, "bash"])

    @mdk_command(name="build")
    def mdk_build():
        """$ docker-compose build [service]"""
        docker_compose(["build", config.service_name])

    @mdk_command(name="down")
    @requires_active_service
    def mdk_down():
        """$ docker-compose down [service]"""
        if not click.confirm(
                "\nDestroying containers for service {}\nProceed?".format(config.service_name),
                default=True):
            sys.exit(0)
        docker_compose(["down"])

    @mdk_command(name="config", hidden="true")
    @click.argument("key", type=click.STRING, required=True)
    @click.argument("val", type=click.STRING, required=True)
    def mdk_config(key, val):
        """set mdk config variable [KEY] to [VAL]"""
        setattr(config, key, val)

    @mdk_command(name="exec")
    @click.argument("command", nargs=-1, type=click.STRING)
    @click.option("-d", "--detach", is_flag=True)
    @requires_active_service
    def mdk_exec(command, detach):
        """$ docker-compose exec [--detach] [service] [command]"""
        exec_command = ["exec", config.service_name]
        docker_compose(exec_command + list(command), detach=detach)
        if detach:
            log.success("Executed {} with service {}".format(
                " ".join(command),
                config.service_name))

    @mdk_command(name="logs")
    @requires_active_service
    def mdk_logs():
        """$ docker-compose logs [service]"""
        docker_compose(["logs", config.service_name])

    @mdk_command(
        name="ls",
        short_help="list docker containers, images, and volumes")
    def mdk_ls():
        """list docker containers, images, and volumes

        $ docker ps -a
        $ docker images
        $ docker volume ls
        """
        log("\nContainers:")
        docker(["ps", "-a"])
        log("\nImages:")
        docker(["images"])
        log("\nVolumes:")
        docker(["volume", "ls"])
        log("")

    @mdk_command(
        name="lsc",
        short_help="list docker containers")
    @click.option("-v", "--verbose", is_flag=True)
    def mdk_lsc(verbose):
        """list docker containers

        $ docker ps -a [--format ...]
        """
        ls_command = ["ps", "-a"]
        if not verbose:
            ls_command.extend([
                "--format",
                "table {{.Names}}\t{{.Image}}\t{{.Status}}"])
        docker(ls_command)

    @mdk_command(
        name="lsi",
        short_help="list docker images")
    @click.option("-v", "--verbose", is_flag=True)
    def mdk_lsi(verbose):
        """list docker images

        $ docker images [--format ...]
        """
        images_command = ["images"]
        if not verbose:
            images_command.extend([
                "--format",
                "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"])
        docker(images_command)

    @mdk_command(
        name="lsv",
        short_help="list docker volumes")
    def mdk_lsv():
        """list docker volumes

        $ docker volume ls
        """
        docker(["volume", "ls"])

    @mdk_command(name="pause")
    @requires_active_service
    def mdk_pause():
        """$ docker-compose pause [service]"""
        docker_compose(["pause", config.service_name])

    @mdk_command(
        name="prune",
        short_help="delete dangling docker assets")
    @click.option("-v", "--volumes", is_flag=True)
    def mdk_prune(volumes):
        """delete dangling containers, images, and (optionally) volumes

        $ docker system prune -a -f [--volumes]
        """
        prune_command = ["system", "prune", "-a", "-f"]
        action_string = "Destroying all inactive containers and unused images."
        if volumes:
            prune_command.append("--volumes")
            action_string = "Destroying all inactive containers, volumes, and unused images."
        if not click.confirm("\n{}\nProceed?".format(action_string), default=True):
            sys.exit(0)

        docker(prune_command)

    @mdk_command(name="run")
    @requires_active_service
    @click.argument("command", nargs=-1, type=click.STRING)
    def mdk_run(command):
        """$ docker-compose run [service] [command]"""
        docker_compose(["run", config.service_name] + list(command))

    @mdk_command(name="start")
    @requires_active_service
    def mdk_start():
        """$ docker-compose start [service]"""
        docker_compose(["start", config.service_name])

    @mdk_command(name="status")
    def mdk_status():
        """print the current active service"""
        log("mdk shared directory:")
        log("  {:12}{}".format("local", config.shared_path_host))
        log("  {:12}{}".format("container", config.shared_path_target))

        if config.service_name is None or config.service_dir is None:
            log("no active service")
            sys.exit(0)

        log("active service:")
        log("  {:12}{}".format("name", config.service_name))
        log("  {:12}{}".format("root", config.service_dir))

        local_compose = utils.parse_yaml(Path.cwd()/"docker-compose.yaml")
        if local_compose is None or \
           "services" not in local_compose or \
           config.service_name not in local_compose["services"]:
            sys.exit(0)

        service_info = local_compose["services"][config.service_name]
        if "container_name" not in service_info:
            log("  please add `container_name` to service config")
            sys.exit(0)

        status_fields = ["Names", "ID", "Status", "Image", "Command", "Size"]
        docker_output = docker([
            "ps", "-a",
            "--format", "{{." + "}},{{.".join(status_fields) + "}}",
            "--filter", "name={}".format(service_info["container_name"]),
        ], detach=True).strip(" \n")

        status_results = docker_output.split(",") if docker_output else None
        if not status_results:
            log("  {:12}{}".format("container", "not created"))
        elif len(status_results) == len(status_fields):
            log("service container:")
            for field in status_fields:
                log("  {:12}{}".format(field, status_results.pop(0)))

        log("autogeneration:")
        log("  {:12}{}".format("status", "active" if config.autogen_active else "inactive"))
        if config.autogen_active and config.autogen_path.exists():
            log("  {:12}{}".format("generated", config.autogen_path.resolve()))
            files = [x for x in config.overrides_dir.iterdir() if x.suffix in [".yml", ".yaml"]]
            file_strings = [x.resolve() for x in files] if files else [""]
            log("  {:12}- {}".format("sources", file_strings.pop()))
            _ = [log("{:14}- {}".format("", x.resolve())) for x in file_strings]

    @mdk_command(name="stop")
    @requires_active_service
    def mdk_stop():
        """$ docker-compose stop [service]"""
        docker_compose(["stop", config.service_name])

    @mdk_command(name="unpause")
    @requires_active_service
    def mdk_unpause():
        """$ docker-compose unpause [service]"""
        docker_compose(["unpause", config.service_name])

    @mdk_command(name="use")
    @click.argument("service", type=click.STRING)
    @click.option(
        "--directory", "-d",
        default=None,
        help="directory containing the service\'s docker-compose.yaml",
        type=str)
    def mdk_use(service, directory):
        """set the active docker-compose service"""
        service_dir = Path.cwd()
        if directory is not None:
            service_dir = Path(directory)
        local_compose = utils.parse_yaml(service_dir/"docker-compose.yaml")
        if local_compose is None:
            log.error("using service", "no docker-compose.yaml in {}.".format(service_dir))
        elif not "services" in local_compose:
            log.error("using service", "no 'services' in docker-compose.yaml")
        elif not service in local_compose["services"]:
            log.error("using service", "service {} not in docker-compose.yaml".format(service))
        else:
            config.service_name = service

            config.service_dir = service_dir.resolve()
            log.success("New active service: {}".format(service))

    @mdk_command(name="up")
    @click.option("-a", "--attach", is_flag=True)
    @click.option("-b", "--build", is_flag=True)
    @click.option("--bash", is_flag=True)
    @requires_active_service
    def mdk_up(attach, build, bash):
        """$ docker-compose up [--build] [--detach] [service]"""
        up_command = ["up"]
        if build:
            up_command.append("--build")
        if not attach:
            up_command.append("-d")
        up_command.append(config.service_name)
        docker_compose(up_command)
        if bash:
            docker_compose(["exec", config.service_name, "bash"])

    @mdk_command(
        name="zsh",
        short_help="attach a zsh shell for the active, running service")
    @requires_active_service
    def mdk_zsh():
        """attach a zsh shell for the active, running service

        $ docker-compose exec [service] zsh"""
        docker_compose(["exec", config.service_name, "zsh"])

    cli(*args, **kwargs)
