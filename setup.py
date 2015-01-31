from setuptools import setup, find_packages


setup(
    name = "pypass",
    version = "0.1",
    packages = ['pypass'],
    # other arguments here...
    entry_points = {
        'console_scripts': [ 
        	'pypass = pypass:main_entry'
        ]
	}
)
