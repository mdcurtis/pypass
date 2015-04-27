from setuptools import setup, find_packages


setup(
    name = "pypass",
    version = "0.2",
    packages = find_packages(),
    
    install_requires = [
      'python-gnupg>=0.3.7',
      'pyyaml>=3.0'
    ],

    entry_points = {
        'console_scripts': [ 
        	'pypass = pypass:main_entry'
        ]
	}
)
