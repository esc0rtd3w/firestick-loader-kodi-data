# service.streamlink.proxy

- Version: **4.0.0**
- Github: [Twilight0/service.streamlink.proxy](https://github.com/Twilight0/service.streamlink.proxy)
- Repo: [repository.twilight0.libs](https://github.com/Twilight0/repo.twilight0.libs)

## Custom streamlink plugins

- They can be used with [script.module.streamlink.plugins](https://github.com/Twilight0/script.module.streamlink.plugins)

## IPTV Simple PVR
```
#EXTINF:-1 tvg-id="" tvg-shift="" tvg-name="" radio="" tvg-logo="example.png" group-title="English",Example
http://127.0.0.1:50165/?url=https%3A%2F%2Fexample.com%2Fexample&q=best
```
[Twilight0/service.streamlink.proxy](https://github.com/Twilight0/service.streamlink.proxy)
- `http://127.0.0.1:50165/?`
*will write the stream into the buffer*
- `http://127.0.0.1:50165/channel.m3u8?`
*will redirect the hls url instead of writing it into the buffer,
it does not work for every stream.*

VIDEO QUALITY
- `q=worst`
*if you want the **best** stream, you don't need to add this*

VIDEO URL
- `url=https://example.com/example`
or
- `url=https%3A%2F%2Fexample.com%2Fexample`

for the best solution the url should be encoded,
you can encode url's with an [urlencoder](https://www.urlencoder.org)

EXAMPLE
```
# before
https://www.youtube.com/watch?v=K59KKnIbIaM
# after
https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DK59KKnIbIaM
```
