import sys
from simonski.pycommon import utils
from simonski.pycommon.ini import IniFile
import concurrent.futures
from blowpipe.logger import Logger
from blowpipe import config
from blowpipe.server import BlowpipeServerConfig
from blowpipe import constants

import os
from blowpipe import model_db



def init(filename:str):
    """
    Initialises
        - blowpipe.cfg file pointed to by filename
        - sqlite database as a sibling file 'blowpipe.db'
        - folder for logs

    this includes
        blowpipe.cfg
        blowpipe.db
        logs/
    :param filename: a path to a blowpipe.cfg file, e..g /Users/YOU/blowpipe/blowpipe.cfg
    :return:
    """

    abs_filename = utils.resolve_file(filename)
    parent_dir, fname = utils.split_file(abs_filename)
    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir)

    content = constants.DEFAULT_CONFIG
    content = content.replace("TOKEN_HTTP_PORT", str(constants.DEFAULT_HTTP_PORT))
    content = content.replace("TOKEN_GRPC_PORT", str(constants.DEFAULT_GRPC_PORT))
    content = content.replace("TOKEN_GRPC_CLIENT_IP", str(constants.DEFAULT_GRPC_CLIENT_IP))
    content = content.replace("TOKEN_GRPC_SERVER_IP", str(constants.DEFAULT_GRPC_SERVER_IP))

    Logger.console("Initialising '" + filename + "'.")
    f = open(abs_filename, 'w')
    f.write(content)
    f.close()

    cfg = IniFile(abs_filename)
    if not os.path.isdir(cfg.get_root_dir()):
        os.makedirs(cfg.get_root_dir())

    Logger.console("Initialising '" + filename + "' ok.")

    log_dirname = cfg.get_root_dir() + "/logs"
    if not os.path.isdir(log_dirname):
        os.makedirs(log_dirname)

    sqlite_filename = "sqlite:///" + cfg.get_root_dir() + "/blowpipe.db"
    db = model_db.DB(cfg, sqlite_filename)
    db.connect()
    db.reset()
    cfg.save()

    Logger.console("Initialised Blowpipe in " + cfg.get_root_dir())
    config = BlowpipeServerConfig(filename)
    return config
