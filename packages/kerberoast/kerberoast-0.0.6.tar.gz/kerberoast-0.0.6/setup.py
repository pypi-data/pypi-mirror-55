from setuptools import setup, find_packages

setup(
	# Application name:
	name="kerberoast",

	# Version number (initial):
	version="0.0.6",

	# Application author details:
	author="Tamas Jos",
	author_email="info@skelsec.com",

	# Packages
	packages=find_packages(),

	# Include additional files into the package
	include_package_data=True,


	# Details
	url="https://github.com/skelsec/kerberoast",

	zip_safe = True,
	#
	# license="LICENSE.txt",
	description="Kerberos security toolkit for Python",

	# long_description=open("README.txt").read(),
	python_requires='>=3.6',
	classifiers=(
		"Programming Language :: Python :: 3.6",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	),
	install_requires=[
		'msldap>=0.2.3',
		'minikerberos>=0.0.9',
		'winsspi;platform_system=="Windows"',
	],

	entry_points={
		'console_scripts': [
			'kerberoast = kerberoast.kerberoast:run',
		],
	}
)
