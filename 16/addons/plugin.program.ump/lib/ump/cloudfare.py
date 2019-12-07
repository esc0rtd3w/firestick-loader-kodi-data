from StringIO import StringIO
import gzip
import re
import time
import urllib2
from socket import setdefaulttimeout
from third import recaptcha
from urlparse import urlparse
import urllib

noredirs=["/cdn-cgi/l/chk_jschl","/cdn-cgi/l/chk_captcha"]
max_sleep=30

def solve_equation(equation):
	try:
		offset = 1 if equation[0] == '+' else 0
		return int(eval(equation.replace('!+[]', '1').replace('!![]', '1').replace('[]', '0').replace('(', 'str(')[offset:]))
	except:
		pass
	
def readzip(err):
	if err.info().get('Content-Encoding') == 'gzip':
		buf = StringIO(err.read())
		f = gzip.GzipFile(fileobj=buf)
		stream = f.read()
	else:
		stream=err.read()
	return stream

def cflogin(new_url,ua,req,opener,tunnel,tmode,cj,cfagents,up):
	r2=urllib2.Request(new_url,headers={"Referer":req._Request__original,"User-agent":ua})
	r2=tunnel.pre(r2,tmode,cj)
	res=opener.open(r2)
	cookies=cj.make_cookies(res,r2)
	for cookie in cookies:
		cj.set_cookie(cookie)
	tunnel.cook(cj,cookies,tmode)
	cj.add_cookie_header(req)
	cfagents[up.netloc]={tmode:ua}
	
	
def check_cfagent(cj,up,tmode,cfagents):
	cval=None
	agent=None
	cdom=up.netloc
	if len(cdom.split("."))==3:
		cdom=".".join(cdom.split(".")[1:])
	for cookie in cj:
		if cdom in cookie.domain and cookie.name=="cf_clearance":
			cval=cookie.value
	if cval:
		agent=cfagents.get(up.netloc,{}).get(tmode,None)
	return agent	

def ddos_open(url,opener,req,data,timeout,cj,cfagents,cflocks,tunnel,tmode):
	up=urlparse(url)	
	cfagent=check_cfagent(cj,up,tmode,cfagents)
	if cfagent:
		req.add_header("User-agent",cfagent)
	setdefaulttimeout(timeout)
	try:
		response=opener.open(req,data,timeout)
	except urllib2.HTTPError, err:
		body=tunnel.post(readzip(err),tmode)
		ua=req.unredirected_hdrs.get("User-agent","")
		for p in ["Content-length","Cookie"]:
			if p in req.headers:
				req.headers.pop(p)
			if p in req.unredirected_hdrs:
				req.unredirected_hdrs.pop(p)
		if err.code == 503 and "/cdn-cgi/l/chk_jschl" in body:
			#new algo is credited to tknorris
			solver_pattern = 'var (?:s,t,o,p,b,r,e,a,k,i,n,g|t,r,a),f,\s*([^=]+)={"([^"]+)":([^}]+)};.+challenge-form\'\);.*?\n.*?;(.*?);a\.value'
			vc_pattern = 'input type="hidden" name="jschl_vc" value="([^"]+)'
			pass_pattern = 'input type="hidden" name="pass" value="([^"]+)'
			init_match = re.search(solver_pattern, body, re.DOTALL)
			vc_match = re.search(vc_pattern, body)
			pass_match = re.search(pass_pattern, body)
			init_dict, init_var, init_equation, equations = init_match.groups()
			vc = vc_match.group(1)
			password = pass_match.group(1)
			varname = (init_dict, init_var)
			result = int(solve_equation(init_equation.rstrip()))
			print 'init: %s = %s' % (init_equation, result)
			for equation in equations.split(';'):
					equation = equation.rstrip()
					if equation[:len('.'.join(varname))] != '.'.join(varname):
							print 'Equation does not start with varname |%s|' % equation
					else:
							equation = equation[len('.'.join(varname)):]
		
					expression = equation[2:]
					operator = equation[0]
					if operator not in ['+', '-', '*', '/']:
						print 'Unknown operator: |%s|' % (equation)
						continue
						
					result = int(str(eval(str(result) + operator + str(solve_equation(expression)))))
					print 'intermediate: %s = %s' % (equation, result)
			
			scheme = up.scheme
			domain = up.hostname
			result += len(domain)
			#credit ends here :)
			print 'Final Result: |%s|' % (result)			
			waittime=float(re.findall("\}\,\s([0-9]*?)\)\;",body)[0])/1000
			print "%s has been stalled for %d seconds due to cloudfare protection"%(err.url,waittime)
			time.sleep(waittime)
			new_url = '%s://%s/cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s&pass=%s' % (scheme, domain, vc, result, urllib.quote(password))
			cflogin(new_url,ua,req,opener,tunnel,tmode,cj,cfagents,up)
			response=opener.open(req,data,timeout)
		elif err.code == 403 and "/cdn-cgi/l/chk_captcha" in body and False:
			hash=re.findall('data-sitekey="(.*?)"',body)[0]
			solver=recaptcha.UnCaptchaReCaptcha()
			token=solver.processCaptcha(hash, ump.backwards.getLanguage(0).lower(), opener,ua,up.netloc+" requires Cloudfare Recaptcha")
			u=up.scheme+"://"+up.netloc+"/cdn-cgi/l/chk_captcha?g-recaptcha-response="+token
			cflogin(u,ua,req,opener,tunnel,tmode,cj,cfagents,up)
			response=opener.open(req,data,timeout)
		else:
			response=opener.open(req,data,timeout)
	return response