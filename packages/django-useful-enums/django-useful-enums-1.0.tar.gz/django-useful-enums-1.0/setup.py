from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    author="Graham Binns",
    author_email="graham@outcoded.dev",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="A useful enumeration / choice library for Django.",
    download_url=(
        "https://github.com/grahambinns/django-useful-enums/archive/1.0.tar.gz"
    ),
    install_requires=["stringcase"],
    keywords=["django", "choices", "enumerations"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="django-useful-enums",
    packages=["usefulenums"],
    setup_requires=["wheel"],
    url="https://github.com/grahambinns/django-useful-enums",
    version="1.0",
)
