"""

systemically set logging part


"""


import os
import logging
import colorlog


logging.basicConfig()
logger = logging.getLogger(__name__)

colorHandler = colorlog.StreamHandler()
colorHandler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(name)s:%(message)s'))

global LOG_ENV_RECORD

LOG_ENV_RECORD = {}


def get_env_logname(name):
    """
    get_env_logname
    """
    modname = name.split('.')[0].upper()
    envname = f"{modname}_LOGLEVEL"
    # print(envname)
    return envname


def get_env_loglevel(envlogname):
    """
    get_env_loglevel
    """
    if envlogname in LOG_ENV_RECORD:
        return LOG_ENV_RECORD[envlogname]
    level = os.environ.get(envlogname, logging.WARNING)
    if isinstance(level, str):
        if level.isdigit():
            level = int(level)
        else:
            level = level.upper()
            level = getattr(logging, level)
    assert isinstance(level, int)
    LOG_ENV_RECORD[envlogname] = level
    levelname = logging.getLevelName(level)
    logger.info(f"{envlogname}: {levelname}")
    return level


def getLogger(name, logtype=None, env_logname=None):
    """
    get Logger
    Input:
        name: name of the module, generally __name__
        logtype: 'normal' or 'color'
        env_logname: name of the environment variable used, default
            is {ROOT_MODULE}_LOGLEVEL
    Output:
        logger handle for logging output
    """
    logtype = logtype or "normal"
    assert logtype in ["normal", "color"]
    if not env_logname:
        env_logname = get_env_logname(name)
    env_loglevel = get_env_loglevel(env_logname)
    if logtype == "normal":
        newlogger = logging.getLogger(name)
    else:
        newlogger = colorlog.getLogger(name)
        newlogger.addHandler(colorHandler)
    newlogger.setLevel(env_loglevel)
    return newlogger
