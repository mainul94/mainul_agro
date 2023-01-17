from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mainul_agro/__init__.py
from mainul_agro import __version__ as version

setup(
	name="mainul_agro",
	version=version,
	description="Customization for Agro",
	author="Mainul Islam",
	author_email="mainulkhan94@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
