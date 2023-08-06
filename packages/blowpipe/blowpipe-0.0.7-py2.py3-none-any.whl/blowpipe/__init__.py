import os
import sys
from blowpipe.client_cli import BlowpipeClient
from blowpipe.config import BlowpipeClientConfig, BlowpipeServerConfig
from blowpipe.server import BlowpipeServer
from blowpipe import bp_utils
from simonski.pycommon import utils
from simonski.pycommon.cli import CLI
from blowpipe import constants
import blowpipe
from blowpipe.logger import Logger
from blowpipe import bootstrap


def init() -> bool:
    """
    initialises the blowpipe.cfg and .db files
    The autodiscover logic will attempt to find in order
    A CLI parameter, the BLOWPIPE_HOME directory or the current directory
    :return:
    """
    filename, dicovery_style = bp_utils.autodiscover_server_config_file("-config", "BLOWPIPE_HOME", "blowpipe.cfg")
    if os.path.isfile(filename):
        # already exists, won't init.
        Logger.console("Error, '" + filename + "' already exists, won't init.")
        sys.exit(1)
    else:
        bootstrap.init(filename)
        Logger.console("Successfully initialised blowpipe at " + filename)
        return True


def server(cli: CLI):
    filename, type_of_file = bp_utils.autodiscover_server_config_file("-config", "BLOWPIPE_HOME", "blowpipe.cfg")
    if not os.path.isfile(filename):
        msg = "Error, Blowpipe server cannot run, no configuration found." \
            + "\nYou must set one of the following:" \
            + "\n" \
            + "\n\t1. $BLOWPIPE_HOME" \
            + "\n\t2. 'blowpipe.cfg' not found in current dir." \
            + "\n\t3. Pass location of config file with '-config' option." \
            + "\n"
        Logger.console(msg)
        sys.exit(1)

    if type_of_file == 1:
        print("Server: using -config parameter '" + filename + "'")
    elif type_of_file == 2:
        print("Server: using $BLOWPIPE_HOME '" + filename + "'")
    elif type_of_file == 3:
        print("Server: using config file '" + filename + "'")

    cfg = BlowpipeServerConfig(filename)
    cfg.is_repository = cli.contains("-repository")

    grpc_ip = cfg.get_grpc_server_ip()
    if grpc_ip == "::":
        grpc_ip = "127.0.0.1"

    if not utils.is_port_available(grpc_ip, cfg.get_grpc_port()):
        # looks like something is running on that port.
        # let's see if we can connect to it as the client; if we can
        # then we will be
        if bp_utils.is_server_running(cfg):
            friendly = cfg.get_grpc_server_ip() + ":" + str(cfg.get_grpc_port())
            print("Error, Blowpipe Server is already running on " + friendly)
        else:
            print("Error, port " + str(cfg.get_grpc_port()) + " already in use by something else.")
        sys.exit(1)
    else:
        bp_utils.print_logo()
        srv = BlowpipeServer(cfg)
        srv.start(blocking=True)


def client(cli:CLI):
    filename, discovery_style = bp_utils.autodiscover_server_config_file("-config", "BLOWPIPE_HOME", "blowpipe.cfg")
    default_filename = utils.resolve_file("~/.blowpipe/blowpipe.cfg")
    if not os.path.isfile(filename):
        if not os.path.isfile(default_filename):
            if blowpipe.constants.VERBOSE:
                Logger.console("No configuration file found - using default client settings.")
            cfg = BlowpipeClientConfig()
        else:
            filename = default_filename
            cfg = BlowpipeClientConfig(filename)
    else:
        cfg = BlowpipeClientConfig(filename)

    default_server = cfg.get_grpc_client_ip() + ":" + str(cfg.get_grpc_port())
    server_url = os.getenv("BLOWPIPE_URL", default_server)
    splits = server_url.split(":")
    hostname = splits[0]
    port = splits[1]

    cfg.set_grpc_server_ip(hostname)
    cfg.set_grpc_port(port)

    cli = bp_utils.CLI()
    client = BlowpipeClient(cfg)
    client.process(cli)


def main():
    cli = CLI(sys.argv)
    blowpipe.logger.CONSOLE_ENABLED = cli.contains("-v")
    blowpipe.constants.VERBOSE = cli.contains("-v")
    if cli.get_command() == "init":
        init()
    elif cli.get_command() == "server":
        server(cli)
    else:
        client(cli)
