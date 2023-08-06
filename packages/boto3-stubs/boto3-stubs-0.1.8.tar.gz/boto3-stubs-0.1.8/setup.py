from pathlib import Path

from setuptools import setup


ROOT_PATH = Path(__file__).absolute().parent


setup(
    name="boto3-stubs",
    version="0.1.8",
    packages=["boto3-stubs"],
    url="https://github.com/vemel/mypy_boto3",
    license="MIT License",
    author="Vlad Emelianov",
    author_email="vlad.emelianov.nz@gmail.com",
    description="Boto3 stubs powered by mypy-boto3.",
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
    long_description=(ROOT_PATH / "README.md").read_text(),
    long_description_content_type="text/markdown",
    package_data={"boto3-stubs": ["py.typed", "__init__.pyi"]},
    install_requires=[f"mypy-boto3==0.1.8"],
    zip_safe=False,
)
