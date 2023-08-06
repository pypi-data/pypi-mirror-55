import logging

from .aria2 import Aria2
from .session import Session
from config import YAMLConfig, Constants
import os
import re
import subprocess
import threading

from m3u8_dl.parser import Parser

logger = logging.getLogger(__name__)


class Downloader(object):

    def __init__(self, session=True):
        self._aria2p = None
        self._m3u8_download_list = None
        self._downloading = False
        self._total_segments = 0
        self._session = session

    @property
    def aria2p(self):
        return self._aria2p

    @property
    def m3u8_download_list(self):
        return self._m3u8_download_list

    def download(self, m3u8s):
        self._m3u8_download_list = Parser.parse(m3u8s)
        if len(m3u8s) == 0:
            logger.info('Download abort: m3u8s is empty and there is nothing to download.')
            return
        logger.info('Get %d download tasks, preparing...' % len(m3u8s))
        if not self.aria2p:
            logger.debug('Aria2c is not running.')
            aria2 = Aria2.get_instance()
            self._aria2p = aria2.start()
        self._downloading = True
        self.aria2p.purge_all()
        for l in self._m3u8_download_list:
            download_dir = Downloader._get_download_dir(l['name'])
            logger.debug(f'{l["name"]} dir: {download_dir}')
            uris = l['segments']
            download_details = []
            for u in uris:
                self._total_segments += 1
                download = self.aria2p.add_uris([u], {
                    'dir': download_dir,
                    'user_agent': Constants.user_agent
                })
                download_details.append(download)
            logger.info(f'\'{l["name"]}\' is added to Aria2.')
        logger.info('All videos are added to Aria2, please wait for completion...')
        self._download_monitor()
        self.listen_to_notifications()

    def listen_to_notifications(self):
        def complete(api, gid):
            active_num = self.aria2p.get_stats().num_active
            if active_num == 0 or not self._downloading:
                logger.debug(f'All downloaded.')
                self._downloading = False

        if self.aria2p.get_stats().num_active == 0:
            logger.info('There is nothing to download, listener will be stopped.')
            self.aria2p.stop_listening()
        else:
            self.aria2p.listen_to_notifications(on_download_complete=complete)
        Aria2.get_instance().shutdown()

    def _download_completed(self):
        # for security, all operations should wait for download monitor closed
        self.aria2p.purge_all()
        self.aria2p.stop_listening()
        self.post_download()
        # save session
        if self._session:
            Session.save(self._m3u8_download_list[0]['name'])

    def _download_monitor(self):
        stats = self.aria2p.get_stats()
        logger.debug('<Aria2p stats> num_active: %s, num_waiting: %s, download_speed: %s' % (
            stats.num_active, stats.num_waiting, stats.download_speed
        ))
        not_completed_num = stats.num_active + stats.num_waiting
        completed_num = self._total_segments - not_completed_num
        completed_percentage = completed_num / self._total_segments * 100
        if stats.download_speed < 1000:
            download_speed = '%.2f B/s' % stats.download_speed
        elif 1000 <= stats.download_speed < 1000000:
            ds = stats.download_speed / 1000
            download_speed = '%.2f KB/s' % ds
        else:
            ds = stats.download_speed / 1000000
            download_speed = '%.2f MB/s' % ds
        logger.info('Complete: %.2f%% (%d/%d), download speed: %s' %
                    (completed_percentage, completed_num, self._total_segments, download_speed))
        if self._downloading and not_completed_num > 0:
            threading.Timer(1.0, self._download_monitor).start()
        else:
            self._downloading = False
            self._download_completed()

    def post_download(self):
        logger.info('performing post download...')
        # check ffmpeg installation status
        outputs = subprocess.check_output('ffmpeg -version', shell=True).decode(Constants.coding)
        if re.search('ffmpeg version', outputs) is None:
            raise Exception('FFmpeg is not installed.')
        # merge *.tz to mp4
        for l in self.m3u8_download_list:
            download_dir = Downloader._get_download_dir(l['name'])
            filename_of_segments = []
            # uri to ts filename, e.g. https://xxx/out000.ts -> out000.ts
            for s in l['segments']:
                filename_of_segments.append(Downloader._uri_to_filename(s))
            # generate merge info
            merge_file = Downloader._generate_ts_merge_info(download_dir, filename_of_segments)
            # merge
            if merge_file is not None:
                Downloader.merge_ts(merge_file, YAMLConfig.get()["aria2"]["download_path"] + os.sep + l["name"] + ".ts")
            # remove temp directory
            subprocess.call(f'rm -rf "{download_dir}"', shell=True)

    @staticmethod
    def _get_download_dir(name):
        return '%s%s%s' % (YAMLConfig.get()['aria2']['download_path'], os.sep, name)

    @staticmethod
    def _uri_to_filename(uri):
        filename = re.search(r'(?<=/hls/\d{4}/\d{2}/\d{2}/\w{8}/).*\.ts$', uri)
        if filename is None:
            raise ValueError(f'{uri} cannot be parsed to ts file')
        filename = filename.group(0)
        logger.debug(f'{uri} is parsed to {filename}')
        return filename

    @staticmethod
    def _generate_ts_merge_info(download_dir, segments):
        merge_file_path = '%s%s%s' % (download_dir, os.sep, 'merge.txt')
        try:
            with open(merge_file_path, 'w') as f:
                for s in segments:
                    f.write(f'file \'{s}\'\n')
            logger.debug(f'merge info has been created at {merge_file_path}')
        except FileNotFoundError:
            logger.error('Merge info not exists: %s' % merge_file_path)
            return None
        return merge_file_path

    @staticmethod
    def merge_ts(merge_file, output):
        cmd = f'ffmpeg -f concat -i "{merge_file}" -c copy "{output}"'
        process = subprocess.Popen(cmd, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()
        errcode = process.returncode
        logger.debug(f'errcode: {errcode}')
        if errcode == 0:
            logger.info(f'Video is merged successfully and saved into: {output}')
        else:
            logger.error(f'FFpmeg error: \n{err.decode(Constants.coding)}')
