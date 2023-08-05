import os.path
import sys

import setuptools

root_dir = os.path.abspath(os.path.dirname(__file__))
readme_file = os.path.join(root_dir, "README.rst")
with open(readme_file, encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="aioice",
    version="0.6.16",
    description="An implementation of Interactive Connectivity Establishment (RFC 5245)",
    long_description=long_description,
    url="https://github.com/aiortc/aioice",
    author="Jeremy Lainé",
    author_email="jeremy.laine@m4x.org",
    license="BSD",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    package_dir={"": "src"},
    package_data={"aioice": ["py.typed"]},
    packages=["aioice"],
    install_requires=["netifaces"],
)
