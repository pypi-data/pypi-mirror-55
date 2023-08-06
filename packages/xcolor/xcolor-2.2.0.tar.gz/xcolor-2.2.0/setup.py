from setuptools import find_packages, setup

setup(
    author = "Max",
    author_email = "max@artsoft.io",
    license = "MIT",
    name = "xcolor",
    version = "2.2.0",
    keywords = "color print ColorPrint python3",
    url = "https://github.com/artsoftio/xcolor",
    install_requires = [],
    py_modules = [],
    packages = find_packages(),
    description = "终端彩色打印",
    long_description = open("README.md").read(),
    long_description_content_type='text/markdown',
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX",
    ]
)