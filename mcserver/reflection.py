"""
A small reflection type helper.
"""

def get_class(klass):
	"""
	Get the class/module object from the class/module name

	Taken with love from:
	http://stackoverflow.com/questions/452969/does-python-have-an-equivalent-to-java-class-forname
	"""

	parts  = klass.split('.')
	module = '.'.join(parts[:-1])
	m      = __import__(module)
	for comp in parts[1:]:
		m = getattr(m, comp)

	return m
