import re

def MultipleReplace(text, dict_):
	
	""" Perform multiple regex replacements at once.

	Parameters
	----------
	text : str
	  Text to use regex on
	dict_ : dict
	  Dictionary where key:value pairs represent original:replacement pairs for the regex
	
	Returns
	-------
	str
	  `text` with replacements made from `dict_`
	"""
       
	regex = re.compile('|'.join(map(re.escape, dict_.keys())))
	return regex.sub(lambda x: dict_[x.string[x.start():x.end()]], text)