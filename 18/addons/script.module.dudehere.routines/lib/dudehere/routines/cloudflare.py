import re
import urllib2
import urlparse
import cookielib
from dudehere.routines import *
from dudehere.routines import plugin

class NoRedirection(urllib2.HTTPErrorProcessor):
	def http_response(self, request, response):
		plugin.log('Stopping Redirect')
		return response

	https_response = http_response

def solve_equation(equation):
	try:
		offset = 1 if equation[0] == '+' else 0
		return int(eval(equation.replace('!+[]', '1').replace('!![]', '1').replace('[]', '0').replace('(', 'str(')[offset:]))
	except:
		pass

def solve(url, cookie_file, user_agent, wait=True):
	headers = {'User-Agent': user_agent, 'Referer': url}
	cj = cookielib.LWPCookieJar(cookie_file)
	if cj is not None:
		try: cj.load(ignore_discard=True)
		except: pass
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)

	request = urllib2.Request(url)
	for key in headers: request.add_header(key, headers[key])
	try:
		response = urllib2.urlopen(request)
		html = response.read()
	except urllib2.HTTPError as e:
		html = e.read()

	
	solver_pattern = 'var (?:s,t,o,p,b,r,e,a,k,i,n,g|t,r,a),f,\s*([^=]+)={"([^"]+)":([^}]+)};.+challenge-form\'\);.*?\n.*?;(.*?);a\.value'
	vc_pattern = 'input type="hidden" name="jschl_vc" value="([^"]+)'
	pass_pattern = 'input type="hidden" name="pass" value="([^"]+)'
	init_match = re.search(solver_pattern, html, re.DOTALL)
	vc_match = re.search(vc_pattern, html)
	pass_match = re.search(pass_pattern, html)

	if not init_match or not vc_match or not pass_match:
		plugin.log("Couldn't find attribute: init: |%s| vc: |%s| pass: |%s| No cloudflare check?" % (init_match, vc_match, pass_match))
		return False
		
	init_dict, init_var, init_equation, equations = init_match.groups()
	vc = vc_match.group(1)
	password = pass_match.group(1)

	# log_utils.log("VC is: %s" % (vc), xbmc.LOGDEBUG)
	varname = (init_dict, init_var)
	result = int(solve_equation(init_equation.rstrip()))
	#plugin.log('Initial value: |%s| Result: |%s|' % (init_equation, result))
	
	for equation in equations.split(';'):
			equation = equation.rstrip()
			if equation[:len('.'.join(varname))] != '.'.join(varname):
				plugin.log('Equation does not start with varname |%s|' % (equation))
			else:
				equation = equation[len('.'.join(varname)):]

			expression = equation[2:]
			operator = equation[0]
			if operator not in ['+', '-', '*', '/']:
				#plugin.log('Unknown operator: |%s|' % (equation))
				continue
				
			result = int(str(eval(str(result) + operator + str(solve_equation(expression)))))
			#plugin.log('intermediate: %s = %s' % (equation, result))
	
	scheme = urlparse.urlparse(url).scheme
	domain = urlparse.urlparse(url).hostname
	result += len(domain)
	#plugin.log('Final Result: |%s|' % (result))

	if wait:
		plugin.log('Sleeping for 5 Seconds')
		plugin.sleep(5000)
			
	url = '%s://%s/cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s&pass=%s' % (scheme, domain, vc, result, password)
	#plugin.log('url: %s' % (url))
	request = urllib2.Request(url)
	for key in headers: request.add_header(key, headers[key])
	try:
		opener = urllib2.build_opener(NoRedirection)
		urllib2.install_opener(opener)
		response = urllib2.urlopen(request)
		while response.getcode() in [301, 302, 303, 307]:
			if cj is not None:
				cj.extract_cookies(response, request)
			request = urllib2.Request(response.info().getheader('location'))
			for key in headers: request.add_header(key, headers[key])
			if cj is not None:
				cj.add_cookie_header(request)
				
			response = urllib2.urlopen(request)
		final = response.read()
	except urllib2.HTTPError as e:
		plugin.log('CloudFlare Error: %s on url: %s' % (e.code, url))
		return False

	if cj is not None:
		cj.save()
		#plugin.log('CF Save Cookies')
		
	return final, cj