import re

pattern = re.compile(r'[vV](?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)')


def increment_version(version, release_type):
	"""Increment a semantic version string

	Returns:
		str -- The incremented semantic version string
	"""
	parts = pattern.match(version).groupdict()
	major = int(parts['major'])
	minor = int(parts['minor'])
	patch = int(parts['patch'])
	
	if (release_type == 'major'):
		major += 1
		minor = 0
		patch = 0
	elif (release_type == 'minor'):
		minor += 1
		patch = 0
	elif (release_type == 'patch'):
		patch += 1
	
	return f'v{major}.{minor}.{patch}'


def boolify(s):
	return str(s).lower() in ['yes', 'y', 'true', '1']
