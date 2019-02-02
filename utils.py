import re

pattern = re.compile(r'(?P<prefix>[vV])(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)')


# TODO: unit test
def increment_version(version, release_type):
	parts = pattern.match(version).groupdict()
	major = int(parts['major'])
	minor = int(parts['minor'])
	patch = int(parts['patch'])
	
	if (release_type == 'major'):
		major += 1
	elif (release_type == 'minor'):
		minor += 1
	elif (release_type == 'patch'):
		patch += 1
	
	return f'v{major}.{minor}.{patch}'
