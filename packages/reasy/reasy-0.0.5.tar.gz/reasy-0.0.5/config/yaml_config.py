import yaml
import logging
import sys
import os

logger = logging.getLogger(__name__)


class YAMLConfig:
    _config = None

    @staticmethod
    def get():
        if YAMLConfig._config is None:
            try:
                with open(os.getenv('REASY_CONFIG', '/.reasy/config.yaml'), 'r') as file:
                    YAMLConfig._config = yaml.safe_load(file)
                    logger.debug('config.yaml: %s' % YAMLConfig._config)
            except FileNotFoundError:
                logging.error('Config is not existed.')
                sys.exit(0)
        return YAMLConfig._config

    @staticmethod
    def session_enabled():
        return YAMLConfig.get()['session']['enabled']

    @staticmethod
    def session_path():
        return YAMLConfig.get()['session']['path']
