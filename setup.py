# scrapper for thepiratebay
# created by Randall Dunn 
try:
    from setuptools import setup
execpt ImportError:
    from distutils.core import setup

config = {
    'description': 'Auto search thepiratebay for <SHOW SXXEYY>',
    'author': 'Randall Dunn',
    'url': 'URLOFSCRIPT',
    'download_url': 'URLOFDOWNLOAD',
    'author_email': 'justthisguyrandall@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['torrentScrapper'],
    'scripts': [],
    'name': 'grabMyTorrents'
}

setup(**config)
    
