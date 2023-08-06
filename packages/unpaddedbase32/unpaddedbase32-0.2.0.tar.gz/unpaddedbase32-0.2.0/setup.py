import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unpaddedbase32",
    version="0.2.0",
    author="Kevin Froman",
    author_email="beardog@mailbox.org",
    description="Enables the ability to use base32 without padding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beardog108/python-unpaddedbase32",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
