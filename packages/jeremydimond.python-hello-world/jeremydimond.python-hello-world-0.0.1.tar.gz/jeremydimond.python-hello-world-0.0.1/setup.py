import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jeremydimond.python-hello-world",
    version="0.0.1",
    author="Jeremy Dimond",
    author_email="jeremy@jeremydimond.com",
    description="hello world",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeremydimond/python-hello-world/archive/release_0_0_1.tar.gz",
    packages=setuptools.find_packages(),
    keywords=['hello world'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
