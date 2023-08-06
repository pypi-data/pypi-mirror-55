import subprocess
import logging
import re
import sys
from config import YAMLConfig, Constants
import aria2p

logger = logging.getLogger(__name__)


class Aria2:
    _instance = None

    def __init__(self):
        if Aria2._instance is not None:
            raise Exception('Aria2 Singleton creation failed, there has a instance already.')
        else:
            self._start_aria2_cmd = None
            self._aria2p = None
            Aria2._instance = self

    @staticmethod
    def get_instance():
        if Aria2._instance is None:
            Aria2()
        return Aria2._instance

    @staticmethod
    def is_installed():
        output = subprocess.check_output('aria2c -v', shell=True).decode(Constants.coding)
        version = re.search(r'(?<=aria2 version )\d\.\d{1,2}\.\d', output)
        if version is None:
            return False
        else:
            logger.debug('Aria2 is installed.')
            return True

    @property
    def start_aria2_cmd(self):
        return self._start_aria2_cmd

    @start_aria2_cmd.setter
    def start_aria2_cmd(self, cmd):
        self._start_aria2_cmd = cmd

    @property
    def pid(self):
        cmd = 'ps -ax | grep aria2c'
        out = subprocess.check_output(cmd, shell=True).decode(Constants.coding)
        processes = out.split('\n')
        # logger.debug('processes: %s' % processes)
        for p in processes:
            if self.start_aria2_cmd is not None and p.find(self.start_aria2_cmd) != -1:
                pid = re.sub(r'(?<=\d{3}) .* %s' % self.start_aria2_cmd, 'AAAAAA', p)
                pid = re.search(r'\d+(?=AAAAAA)', pid)
                if pid is not None:
                    pid = pid.group(0)
                    logging.debug('PID of Aria2: %s' % pid)
                    return pid
        return False

    def start(self):
        # check the status of aria2c installation
        if Aria2.is_installed() is False:
            logger.error('Aria2 is not installed.')
            sys.exit(0)
        # not start repeatedly if aria2c has already started
        if self.pid:
            logger.debug('aria2c is running and it will return aria2p directly')
            return self.aria2p
        # start
        config = YAMLConfig.get()
        cmd = 'aria2c --conf-path=%s -D' % config['aria2']['config']
        logger.debug('command of starting aria2: %s' % cmd)
        logger.info('Starting Aria2...')
        out = subprocess.check_output(cmd, shell=True).decode(Constants.coding)
        logger.debug('outputs of starting aria2: %s' % out)
        if out != '':
            logger.error('aria2 start failed: %s' % out)
            raise Exception('aria2 start failed: %s' % out)
        else:
            self.start_aria2_cmd = cmd
            if not self.pid:
                raise Exception('Aria2c has gone away')
        return self.aria2p

    def shutdown(self):
        pid = self.pid
        if pid:
            logger.info('Shutting down Aria2c(PID: %s)...' % pid)
            self._aria2p = None
            subprocess.call('kill %s' % pid, shell=True)

    @property
    def aria2p(self):
        if self._aria2p is None:
            if not self.pid:
                logger.error('Aria2p creation failed: Aria2c is not running.')
                return
            aria2_client = aria2p.Client(host='http://localhost', port=6800)
            self._aria2p = aria2p.API(aria2_client)
        return self._aria2p
