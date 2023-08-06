# -*- coding: utf-8 -*-
'''
wheelz -- complexity via Burrows-Wheeler transform
'''
import functools
import locale
import logging
import sys
from datetime import datetime
from pathlib import Path
#
# third-party imports
#
import click
import coverage
#
# package imports
#
from .version import version as VERSION
#
# start coverage
#
coverage.process_startup()
#
# set locale so grouping works
#
for localename in ['en_US', 'en_US.utf8', 'English_United_States']:
    try:
        locale.setlocale(locale.LC_ALL, localename)
        break
    except locale.Error:
        continue
#
# global constants
#
PROGRAM_NAME='wheelz'
AUTHOR = 'Joel Berendzen'
EMAIL = 'joelb@ncgr.org'
COPYRIGHT = """Copyright (C) 2019, NCGR. All rights reserved.
"""
LOG_DIR = 'logs'
LOG_PATH = Path('.') / LOG_DIR
# defaults for command line
DEFAULT_FILE_LOGLEVEL = logging.DEBUG
DEFAULT_STDERR_LOGLEVEL = logging.INFO
#
# Class definitions.
#
class CleanInfoFormatter(logging.Formatter):
    def __init__(self, fmt='%(levelname)s: %(message)s'):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        if record.levelno == logging.INFO:
            return record.getMessage()
        return logging.Formatter.format(self, record)
#
# time stamp for start
#
STARTTIME = datetime.now()
#
# global logger object
#
logger = logging.getLogger(PROGRAM_NAME)
#
# private context function
#
_ctx = click.get_current_context
#
# Helper functions
#
def init_dual_logger(file_log_level=DEFAULT_FILE_LOGLEVEL,
                     stderr_log_level=DEFAULT_STDERR_LOGLEVEL):
    '''Log to stderr and to a log file at different levels
    '''
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            global logger
            # find out the verbose/quiet level
            if _ctx().params['verbose']:
                _log_level = logging.DEBUG
            elif _ctx().params['quiet']:
                _log_level = logging.ERROR
            else:
                _log_level = stderr_log_level
            logger.setLevel(file_log_level)
            stderrHandler = logging.StreamHandler(sys.stderr)
            stderrFormatter = CleanInfoFormatter()
            stderrHandler.setFormatter(stderrFormatter)
            stderrHandler.setLevel(_log_level)
            logger.addHandler(stderrHandler)
            if _ctx().params['log']:  # start a log file in LOG_PATH
                logfile_path = LOG_PATH / (PROGRAM_NAME + '.log')
                if not LOG_PATH.is_dir():  # create LOG_PATH
                    try:
                        logfile_path.parent.mkdir(mode=0o755, parents=True)
                    except OSError:
                        logger.error('Unable to create log directory "%s"',
                                     logfile_path.parent)
                        raise OSError
                else:
                    if logfile_path.exists():
                        try:
                            logfile_path.unlink()
                        except OSError:
                            logger.error('Unable to remove log file "%s"',
                                         logfile_path)
                            raise OSError
                logfileHandler = logging.FileHandler(str(logfile_path))
                logfileFormatter = logging.Formatter(
                    '%(levelname)s: %(message)s')
                logfileHandler.setFormatter(logfileFormatter)
                logfileHandler.setLevel(file_log_level)
                logger.addHandler(logfileHandler)
            logger.debug('Command line: "%s"', ' '.join(sys.argv))
            logger.debug('%s version %s', PROGRAM_NAME, VERSION)
            logger.debug('Run started at %s', str(STARTTIME)[:-7])
            return f(*args, **kwargs)
        return wrapper
    return decorator


def init_user_context_obj(initial_obj=None):
    '''Put info from global options into user context dictionary
    '''
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            global config_obj
            if initial_obj is None:
                _ctx().obj = {}
            else:
                _ctx().obj = initial_obj
            ctx_dict = _ctx().obj
            if _ctx().params['verbose']:
                ctx_dict['logLevel'] = 'verbose'
            elif _ctx().params['quiet']:
                ctx_dict['logLevel'] = 'quiet'
            else:
                ctx_dict['logLevel'] = 'default'
            return f(*args, **kwargs)
        return wrapper
    return decorator


@click.group(epilog=AUTHOR + ' <' + EMAIL + '>. ' + COPYRIGHT)
@click.option('--warnings_as_errors', is_flag=True, show_default=True,
              default=False, help='Warnings cause exceptions.')
@click.option('-v', '--verbose', is_flag=True, show_default=True,
              default=False, help='Debug info to stderr.')
@click.option('-q', '--quiet', is_flag=True, show_default=True,
              default=False, help='Suppress logging to stderr.')
@click.option('--log/--no-log', is_flag=True, show_default=True,
              default=True, help='Write analysis in ./' + LOG_DIR + '.')
@click.version_option(version=VERSION, prog_name=PROGRAM_NAME)
@init_dual_logger()
@init_user_context_obj()
def cli(warnings_as_errors, verbose, quiet, log):
    """wheelz -- calculate complexity via Burrows-Wheeler transform

    If COMMAND is present, and --no_log was not invoked,
    a log file named wheelz-COMMAND.log
    will be written in the ./logs/ directory.
    """
    if warnings_as_errors:
        logger.debug('Runtime warnings (e.g., from pandas) will cause exceptions')
        warnings.filterwarnings('error')


# other cli components import here
from .core import complexity
