import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WiPi",
    version="0.0.5.dev",
    author="Ryan Chaiyakul",
    description="A general use class based WPA network manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryanchaiyakul/WiPi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
