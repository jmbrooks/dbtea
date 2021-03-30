from pathlib import Path
from setuptools import setup, find_packages

from dbtea import __version__

here = Path(__file__).parent.resolve()

# Get the long description from the README file
with (here / "README.md").open(encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="dbtea",
    description="A command-line tool for helping administer, ",
    version=__version__,
    py_modules=["dbtea"],
    packages=find_packages(exclude=["docs", "tests*", "scripts"]),
    include_package_data=True,
    install_requires=[
        "dbt",
        "PyYAML"
    ],
    tests_require=[
        "black",
        "flake8",
        "isort",
        "mypy",
        "pytest",
        "pytest-cov"
    ],
    entry_points={"console_scripts": ["dbtea = dbtea.core.cli:main"]},
    author="Johnathan Brooks",
    author_email="jb@4mile.io",
    url="https://github.com/4mile/dbtea",
    download_url="https://github.com/4mile/dbtea/tarball/" + __version__,
    classifiers=[
        "",
        ""
    ],
    keywords="dbt developer tools productionization lookml",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
