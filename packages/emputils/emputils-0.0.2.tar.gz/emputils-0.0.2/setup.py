import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="emputils", # Replace with your own username
    version="0.0.2",
    author="David Monk",
    author_email="davidgabrialmonk@cern.ch",
    description="A utility package for working with the EMP framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/dmonk/emputils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
