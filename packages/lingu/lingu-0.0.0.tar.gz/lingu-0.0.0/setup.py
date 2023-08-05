import setuptools
import sys

if sys.version_info < (3, 6):
    print("Reynir requires Python >= 3.6")
    sys.exit(1)


setuptools.setup(
    name="lingu",
    version="0.0.0",
    author="Lingu ehf",
    author_email="egillanton@live.com",
    description="Natural Language Processing library for icelandic",
    long_description="Lingu is a Python package for natural language processing for icelandic.",
    url="https://www.lingu.is",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Natural Language :: Icelandic",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords=["nlp", "icelandic"],
    python_requires='>=3.6',
)
