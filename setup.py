import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="releasify",
    version="0.7.0",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/steven-mercatante/releasify",
    author="Steven Mercatante",
    author_email="steven.mercatante@gmail.com",
    packages=["releasify"],
    include_package_data=True,
    install_requires=["requests"],
)
