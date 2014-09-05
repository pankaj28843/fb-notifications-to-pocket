import os

from pylibmc import Client

os.environ['MEMCACHE_SERVERS'] = os.environ.get(
    'MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

pylibmc_client = Client(
    os.environ['MEMCACHE_SERVERS'],
    username=os.environ['MEMCACHE_USERNAME'],
    password=os.environ['MEMCACHE_PASSWORD']
)
