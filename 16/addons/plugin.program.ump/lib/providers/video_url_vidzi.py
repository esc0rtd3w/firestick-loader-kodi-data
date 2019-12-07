import re
from third import unpack


domain="http://vidzi.tv/"

def run(hash,ump,referer=None):
	src = ump.get_page(domain+hash,"utf8",referer=referer)
	packed=re.findall("script type='text/javascript'\>(eval\(function\(p.*?)\n</script>",src)
	data= unpack.unpack(packed[0]).encode("ascii","ignore").replace("\\","")
	files=re.findall('file:"([^,]*?)"}',data)
	return {"vid":{"url":files[0],"referer":domain+hash}}