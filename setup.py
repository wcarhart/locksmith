import setuptools

with open('README.md', 'r') as fh:
	long_description = fh.read()

setuptools.setup(
	name='locksmith',
	version='0.4',
	author='Will Carhart',
	author_email='wcarhart@sandiego.edu',
	description='Your liaison between repository secrets and the great beyond.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/wcarhart/locksmith',
	packages=['locksmith']
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	license="MIT"
)