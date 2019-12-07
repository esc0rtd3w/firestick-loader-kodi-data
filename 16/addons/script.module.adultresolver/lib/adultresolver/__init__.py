import resolver

def resolve(url, addon_id='', pattern=None):
    u = resolver.streamer().resolve(url, addon_id, pattern)
    return u