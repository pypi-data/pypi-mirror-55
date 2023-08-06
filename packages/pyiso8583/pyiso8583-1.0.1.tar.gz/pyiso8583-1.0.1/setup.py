from setuptools import find_packages, setup
from iso8583 import __version__

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]

if __name__ == "__main__":

    with open('README.rst') as f:
        readme = f.read()

    setup(
        name="pyiso8583",
        version=__version__,
        author="Konstantin Novichikhin",
        author_email="konstantin.novichikhin@gmail.com",
        description="A serializer and deserializer of ISO8583 data.",
        long_description=readme,
        url="https://github.com/manoutoftime/pyiso8583",
        packages=['iso8583'],
        classifiers=classifiers,
        python_requires='>=3.6',
        keywords='iso8583 8583',
    )