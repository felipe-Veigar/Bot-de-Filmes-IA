import time

_cache = {}

def get_cache(key):
    item = _cache.get(key)
    if item and (time.time() - item['timestamp'] < 86400):
        return item['data']
    return None

def set_cache(key, data):
    _cache[key] = {'data': data, 'timestamp': time.time()}