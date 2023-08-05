import os
from setuptools import setup


def find_stubs(package):
    stubs = []
    for root, dirs, files in os.walk(package):
        for f in files:
            stubs.append(os.path.relpath(os.path.join(root, f), package))
    return {package: stubs}


setup(
    name="gst-python-stubs",
    url="https://github.com/miurahr/gst-python-stubs",
    author="Hiroshi Miura",
    author_email="miurahr@linux.com",
    version="0.0.2",
    package_data=find_stubs("gi-stubs"),
    packages=["gi-stubs"],
    install_requires=["PyGObject", 'PyGObject-stubs'],
)
