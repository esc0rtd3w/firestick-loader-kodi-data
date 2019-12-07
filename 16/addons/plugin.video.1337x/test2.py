# coding: utf-8
url = 'https://torrentz.eu/801b79cecfd6d04ba42dadea121dc6cd65363c88'
hash = url[url.rfind('/')+1:]
magnet = 'magnet:?xt=urn:btih:%s' % hash
print magnet