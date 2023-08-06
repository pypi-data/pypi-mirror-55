from collections import OrderedDict

import requests
import logging
from config import Constants, YAMLConfig

import re

from m3u8_dl import Session

logger = logging.getLogger(__name__)


class Collector:

    boundary_str = 'PvgqibigcrE8PgXs'

    headers = OrderedDict(
        (
            ("Host", None),
            ("Connection", "keep-alive"),
            ("Upgrade-Insecure-Requests", "1"),
            ("User-Agent", Constants.user_agent),
            (
                "Accept",
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
                "q=0.8,application/signed-exchange;v=b3",
            ),
            ("Accept-Encoding", "gzip, deflate"),
            ("Accept-Language", "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"),

        )
    )

    @staticmethod
    def get_name_and_details_url(html):
        html = re.sub(r'(?<=<a href="html_data/\d{3}/\d{4}/\d{7}\.html") id="\w{14}">', Collector.boundary_str, html)
        logger.debug(f'reasy html with boundary str: \n{html}')
        details_url = re.findall(r'(?<=<a href=")html_data.*?(?="%s)' % Collector.boundary_str, html)
        name = re.findall(r'(?<=%s).*?(?=</a>)' % Collector.boundary_str, html)
        if len(details_url) != len(name):
            logger.error(f'name arr: {name}')
            logger.error(f'details_url: {details_url}')
            raise Exception('regular process for name and details_url failed: the length of them is not equal.')
        name_and_details_url_arr = []
        for i in range(len(details_url)):
            name_and_details_url_arr.append({
                'name': name[i],
                'details_url': '%s%s%s' % (Constants.bt7086_url, '/', details_url[i])
            })
        logger.debug(f'name_and_details_url_arr: {name_and_details_url_arr}')
        return name_and_details_url_arr

    @staticmethod
    def get_m3u8(url):
        logger.info('Reasy is getting video id from \'%s\'' % url)
        response = requests.get(url=url, headers=Collector.headers)
        if response.status_code != 200:
            raise Exception('BT7086 is unreachable, please check out your network.')
        html = response.content.decode(Constants.coding)
        # logger.debug(f'reasy details html: \n{html}')
        m3u8_id = re.search(r'(?<=/\?id=).*?(?=")', html)
        if m3u8_id is None:
            raise Exception(f'm3u8 id cannot be found in {url}')
        m3u8_id = m3u8_id.group(0)
        logger.debug(f'm3u8 id({m3u8_id}) is get from {url}')
        return m3u8_id

    @staticmethod
    def get_m3u8s(session=True, maximum_download_num=30):
        logger.info('Getting m3u8s from BT7086...')
        response = requests.get(url=Constants.bt7086_url + '/thread.php?fid=111', headers=Collector.headers)
        if response.status_code != 200:
            raise Exception('BT7086 is unreachable, please check out your network.')
        html = response.content.decode(Constants.coding)
        logger.debug(f'BT7086 html: \n{html}')
        name_and_details_url_arr = Collector.get_name_and_details_url(html)
        m3u8s = []
        if len(name_and_details_url_arr) > maximum_download_num:
            logger.info('M3u8s will be cut off: the length is greater than %d (maximum_download_num).'
                        % maximum_download_num)
            name_and_details_url_arr = name_and_details_url_arr[:maximum_download_num]
        last_download_item = None
        if session:
            last_download_item = Session.read()
        for i in name_and_details_url_arr:
            if session and last_download_item is not None and last_download_item == i["name"]:
                logger.info('Detect repeated download item: all download tasks after \'%s\' will be cancelled.'
                            % last_download_item)
                break
            logger.debug(f'name: {i["name"]}\ndetails_url: {i["details_url"]}')
            m3u8_id = Collector.get_m3u8(i["details_url"])
            m3u8_url = 'https://m3u8.cdnpan.com/%s.m3u8' % m3u8_id
            m3u8s.append({
                'name': i["name"],
                'url': m3u8_url
            })
        logger.debug(f'm3u8s: {m3u8s}')
        return m3u8s
