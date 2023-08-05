import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mazgi-sandbox-4d36b809",
    version="0.0.1",
    author="Hidenori MATSUKI",
    author_email="dev@mazgi.com",
    description="Example PKG",
    entry_points={
        "console_scripts": [
            "mazgi-sandbox-4d36b809=mazgi_sandbox_4d36b809.main:main"
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mazgi-sandbox/201911.spike.python-pkg",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        "pyyaml"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
)
