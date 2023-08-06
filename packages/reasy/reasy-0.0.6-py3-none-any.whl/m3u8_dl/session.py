import logging
from config import YAMLConfig, Constants
import os
import base64

logger = logging.getLogger(__name__)


class Session:

    @staticmethod
    def read():
        if not YAMLConfig.session_enabled():
            logger.debug('session is disabled.')
            return None
        if not os.path.isfile(YAMLConfig.session_path()):
            logger.error('session file not exists, please create it before using.')
            raise FileNotFoundError('session file not exists.')
        with open(YAMLConfig.session_path(), 'rb') as f:
            encoded_bytes = f.read()
            content = base64.b64decode(encoded_bytes).decode(Constants.coding)
            logger.debug('content of session: %s' % content)
            return content

    @staticmethod
    def save(name):
        if not YAMLConfig.session_enabled():
            logger.debug('session is disabled.')
            return None
        if not os.path.isfile(YAMLConfig.session_path()):
            logger.error('session file not exists, please create it before using.')
            raise FileNotFoundError('session file not exists.')
        with open(YAMLConfig.session_path(), 'wb') as f:
            encoded_bytes = name.encode(Constants.coding)
            f.write(base64.b64encode(encoded_bytes))
            return True

    @staticmethod
    def clear():
        Session.save('')
