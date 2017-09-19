def tag(word):
	assert isinstance(word,basestring),'argument to tag() must be a string'
	if word in ['a','the']:
		return 'det'
	else:
		return 'noun'
		