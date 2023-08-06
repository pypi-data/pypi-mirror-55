import m3u8
import re
import logging
import time

logger = logging.getLogger(__name__)


class Parser(object):

    @staticmethod
    def m3u8_url_to_download_link_array(url):
        logger.info('\'%s\' is loading...' % url)
        start_time = time.time()
        m3u8_obj = m3u8.load(url)
        duration = (time.time() - start_time) * 1000
        logger.info('\'%s\' is loaded, the process costs %.2f ms' % (url, duration))
        segments = []
        for s in m3u8_obj.segments:
            segments.append(s.uri)
        logger.debug('\'%s\' is converted to %s' % (url, segments))
        if len(segments) == 0:
            logger.error('\'%s\' can\'t would be skipped because it couldn\'t be loaded by m3u8 module.' % url)
            return None
        return segments

    @staticmethod
    def check_m3u8s(m3u8s):
        for i in m3u8s:
            if 'name' not in i:
                raise KeyError('Name for every item of m3u8_list is required.')
            if 'url' not in i:
                raise KeyError('Url for every item of m3u8_list is required.')
            if re.search(r'^https?://.*\.m3u8$', i['url']) is None:
                raise ValueError('Url format is invalid, url: %s' % i['url'])
        logger.debug('Format of m3u8s is acceptable.')
        return True

    @staticmethod
    def parse(m3u8s):
        Parser.check_m3u8s(m3u8s)
        download_list = []
        for m in m3u8s:
            name = m['name']
            url = m['url']
            segments = Parser.m3u8_url_to_download_link_array(url)
            if segments is not None:
                download_list.append({
                    'name': name,
                    'segments': segments
                })
        logger.debug('parsing results of m3u8 list: %s' % download_list)
        return download_list
