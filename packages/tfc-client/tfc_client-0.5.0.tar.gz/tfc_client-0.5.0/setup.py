import os
import setuptools
import sys

from tfc_client import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()

# 'setup.py publish' shortcut.
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()

setuptools.setup(
    name="tfc_client",
    version=__version__,
    author="Alexandre Dath for ADEO",
    author_email="alex.dath@gmail.com",
    license="MIT",
    keywords="API Terraform TFC",
    description="A developer friendly Terraform Cloud API client",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/adeo/iwc-tfc-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    # setup_requires=["pytest-runner"],
    extras_require={
        "dev": ["black", "twine", "wheel"],
        "test": ["pytest", "coverage", "pytest-cov"],
    },
    tests_require=["pytest", "pytest-cov"],
    install_requires=[
        "requests",
        "pydantic",
        "pydantic[email]",
        "email-validator>=1.0.3",
        "idna>=2.0.0",
        "dnspython>=1.15.0",
        "inflection",
    ],
)
