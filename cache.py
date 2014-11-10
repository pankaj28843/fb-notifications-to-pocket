import os

from pylibmc import Client

servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
servers = map(lambda s: s[0], map(lambda x: x.split(':'), servers))

pylibmc_client = Client(
    servers,
    binary=True,
)
