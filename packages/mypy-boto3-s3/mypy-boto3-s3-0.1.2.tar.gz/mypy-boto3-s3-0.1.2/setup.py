from setuptools import setup

from mypy_boto3_s3.version import __version__ as version

with open("../../README.md", "r") as f:
    long_description = f.read()

setup(
    name="mypy-boto3-s3",
    version=version,
    packages=["mypy_boto3_s3"],
    url="https://github.com/vemel/mypy_boto3",
    license="MIT License",
    author="Vlad Emelianov",
    author_email="vlad.emelianov.nz@gmail.com",
    description="Mypy-friendly boto3 type annotations for s3 service.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Typing :: Typed",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"mypy_boto3_s3": ["py.typed"]},
    zip_safe=False,
)
