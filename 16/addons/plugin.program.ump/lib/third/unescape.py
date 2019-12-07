import htmlentitydefs
import re


def unescape(text):
	"""Removes HTML or XML character references 
	and entities from a text string.
	@param text The HTML (or XML) source text.
	@return The plain text, as a Unicode string, if necessary.
	from Fredrik Lundh
	2008-01-03: input only unicode characters string.
	http://effbot.org/zone/re-sub.htm#unescape-html
	"""
	def fixup(m):
		text = m.group(0)
		if text[:2] == "&#":
		# character reference
			try:
				if text[:3] == "&#x":
					return unichr(int(text[3:-1], 16))
				else:
					return unichr(int(text[2:-1]))
			except ValueError:
				pass
		else:
		# named entity
		# reescape the reserved characters.
			try:
				if text[1:-1] == "amp":
					text = "&amp;amp;"
				elif text[1:-1] == "gt":
					text = "&amp;gt;"
				elif text[1:-1] == "lt":
					text = "&amp;lt;"
				else:
					text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
			except KeyError:
				pass
		return text # leave as is
	return re.sub("&#?\w+;", fixup, text)