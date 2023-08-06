from setuptools import setup, find_namespace_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hlfbt-serial-console",
    version="0.0.2",
    author="Alexander Schulz",
    author_email="alex@nope.bz",
    description="A simple utility to interface with prompt-like (serial) consoles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hlfbt/serial_console",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Communications",
        "Topic :: Terminals :: Serial"
    ],
    python_requires='>=3.5',
    packages=find_namespace_packages(include=['hlfbt.*']),
    install_requires=['pyserial']
)
