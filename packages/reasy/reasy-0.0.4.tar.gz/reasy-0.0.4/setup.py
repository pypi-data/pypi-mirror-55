from setuptools import setup, find_packages
from os.path import dirname, abspath, join
from version import __version__ as version

install_reqs = [req for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]

setup(
    name='reasy',
    version=version,
    author='dekofejld',
    author_email='dekofejld@gmail.com',
    py_modules=['reasy', 'version', 'm3u8-dl', 'config', 'collector'],
    packages=find_packages(),
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=install_reqs,
    description="A tool for quick downloading videos from BT7086",
    entry_points='''
        [console_scripts]
        reasy=reasy:cli
    ''',
)
