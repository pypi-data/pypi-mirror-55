from setuptools import setup, find_packages
import pack2048
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='pack2048',
    version=pack2048.__version__,
    packages=find_packages(),
    author="Jérémy Duron",
    author_email="jlmncddgg@gmail.com",
    description="Un module pour résoudre le 2048",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    #url='http://github.com/',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    license="GNU AGPLv3 License",
 
)