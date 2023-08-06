import click
import logging
from m3u8_dl.downloader import Downloader
from collector import Collector
from version import __version__ as ver
import logging

logger = logging.getLogger(__name__)


def verbose_callback(ctx, param, value):
    if value:
        click.echo('Enables verbose.')
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.DEBUG,
        )
    else:
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO,
        )


@click.group()
@click.version_option(None, '-v', '--version', message='reasy version %s' % ver)
def cli():
    pass


@cli.command()
@click.option('--no-session',
              is_flag=True,
              help='Disable session which prevents from repeated download.')
@click.option('--verbose',
              is_flag=True,
              expose_value=False, is_eager=True,
              callback=verbose_callback)
def run(no_session):
    session = not no_session
    if no_session:
        click.echo('Session has been disabled.')
    dl = Downloader()
    dl.download(Collector.get_m3u8s(session), session=session)
