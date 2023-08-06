import yaml
import logging
import sys
import os
from .constants import Constants

logger = logging.getLogger(__name__)


class YAMLConfig:
    _config = None

    @staticmethod
    def get():
        if YAMLConfig._config is None:
            try:
                with open(os.getenv('BT7086_CONFIG', '/.reasy/config.yaml'), 'r') as file:
                    YAMLConfig._config = yaml.safe_load(file)
                    logger.debug('config.yaml: %s' % YAMLConfig._config)
            except FileNotFoundError:
                logging.error('Config is not existed.')
                sys.exit(0)
        return YAMLConfig._config

    @staticmethod
    def maximum_download_num():
        return YAMLConfig.get()['maximum_download_num']

    @staticmethod
    def session_enabled():
        return YAMLConfig.get()['session']['enabled']

    @staticmethod
    def session_path():
        return YAMLConfig.get()['session']['path']
