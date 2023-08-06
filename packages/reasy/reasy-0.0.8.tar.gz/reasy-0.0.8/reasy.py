import click
import logging
from m3u8_dl.downloader import Downloader
from collector import Collector
from version import __version__ as ver
import logging

logger = logging.getLogger(__name__)

banner = """
       ____                           
      / __ \ ___   ____ _ _____ __  __
     / /_/ // _ \ / __ `// ___// / / /
    / _, _//  __// /_/ /(__  )/ /_/ / 
   /_/ |_| \___/ \__,_//____/ \__, /  
                             /____/              
   :: Running Reasy v%s ::
    """ % ver


def echo_banner():
    click.echo(banner)


@click.group()
@click.version_option(None,
                      '-v', '--version',
                      message='reasy version %s' % ver)
def cli():
    pass


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


@cli.command()
@click.option('--no-session',
              is_flag=True,
              help='Disable session, which may cause repeated download.')
@click.option('--max-dl-num', '-m',
              default=30,
              type=int,
              help='Maximum download number per performing, default: 30.')
@click.option('--verbose',
              is_flag=True,
              expose_value=False,
              is_eager=True,
              callback=verbose_callback,
              help='Enables verbose.')
def run(no_session, max_dl_num):
    echo_banner()
    session = not no_session
    # if no_session:
    #     click.echo('Session has been disabled.')
    dl = Downloader(session=session)
    m3u8s = Collector.get_m3u8s(session, max_dl_num)
    dl.download(m3u8s)
