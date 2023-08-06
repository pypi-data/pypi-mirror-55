import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyxag",
    version="0.0.1",
    author="David Doret",
    author_email="david.doret@me.com",
    description="Hobby research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daviddoret/pynag/wiki",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
