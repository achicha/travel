import os
import sys
import getpass
import logging
from functools import lru_cache, wraps
from datetime import datetime as dt


def singleton(cls):
    """sigleton"""
    instance = None

    @wraps(cls)
    def inner(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance
    return inner


@singleton
class LogMixin:
    def __init__(self, parser_name, level='INFO'):
        self.level = level
        self.parser_name = parser_name
        self.logger = logging.getLogger(sys.argv[0].split('/')[-1].split('.')[0])
        self._add_handlers()

    def _add_handlers(self):
        if not self.logger.handlers:
            # create log folder nearby our executable script and define log_filename
            log_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'logs')
            os.makedirs(log_path, 0o777, exist_ok=True)
            log_filename = os.path.join(log_path,
                                        self.parser_name + "_{}.log"
                                        .format(dt.strftime(dt.now(), '%Y%m')))

            # create log file, with 766 permissions for cron
            if not os.path.isfile(log_filename):
                os.mknod(log_filename, mode=0o766)
            # logging level
            lvl = {'INFO': logging.INFO,
                   'DEBUG': logging.DEBUG,
                   'ERROR': logging.ERROR}
            # set defaults
            self.logger.setLevel(logging.DEBUG)
            formatter = self.parser_name + '|%(levelname)s ' + \
                        '[%(asctime)s] [LINE:%(lineno)d %(funcName)s()] >>> %(message)s'
            file_handler = logging.FileHandler(filename=log_filename,
                                               mode='a')
            file_handler.setLevel(lvl[self.level])
            file_handler.setFormatter(logging.Formatter(formatter))
            self.logger.addHandler(file_handler)

            # set second handler
            if self.logger.handlers[0].level > 10:
                # todo: sent email here
                mail_handler = logging.StreamHandler()
            else:
                mail_handler = logging.StreamHandler()

            mail_handler.setLevel(logging.ERROR)
            mail_handler.setFormatter(logging.Formatter(formatter))
            self.logger.addHandler(mail_handler)

            # write init config to *.log file
            self.logger.info('==================================================')
            self.logger.info('script is started at {} UTC'.format(
                dt.strftime(dt.utcfromtimestamp(int(dt.now().timestamp())), '%Y-%m-%d %H:%M:%S')
            ))
            self.logger.info('run by user: {}'.format(getpass.getuser()))
