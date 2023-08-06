import os.path

from setuptools import find_packages, setup

# single source of truth for package version
version_ns = {}
with open(os.path.join("src", "globus_sdk_tokenstorage", "version.py")) as f:
    exec(f.read(), version_ns)  # nosec

setup(
    name="globus-sdk-tokenstorage",
    version=version_ns["__version__"],
    description="Globus SDK TokenStorage Extension",
    long_description=open("README.rst").read(),
    author="Stpehen Rosen",
    author_email="sirosen@globus.org",
    url="https://github.com/globus/globus-sdk-python-tokenstorage",
    packages=find_packages("src", exclude=["tests", "tests.*"]),
    package_dir={"": "src"},
    install_requires=["globus-sdk>=1.6.1,<2"],
    extras_require={
        "test": [
            # testing
            "pytest>=3.7.4,<4.0",
            "pytest-cov>=2.5.1,<3.0",
            "pytest-xdist>=1.22.5,<2.0",
            # mock on py2, py3.4 and py3.5
            # not just py2: py3 versions of mock don't all have the same
            # interface!
            'mock==2.0.0;python_version<"3.6"',
        ]
    },
    include_package_data=True,
    keywords=["globus", "sdk", "contrib"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
