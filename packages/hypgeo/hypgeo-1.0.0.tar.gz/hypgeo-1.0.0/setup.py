import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hypgeo", # Replace with your own username
    version="1.0.0",
    author="Daniel Berger",
    author_email="daniel.berger@l-p-a.com",
    description="Small library for simple algebraic and geometric operations on the upper half plane, such as Moebius transformations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BgDaniel/hpygeo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)