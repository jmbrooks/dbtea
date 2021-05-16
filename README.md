[![CircleCI](https://img.shields.io/circleci/build/github/joshtemple/lkml.svg)](https://circleci.com/gh/jmbrooks/dbtea)
[![Codecov](https://img.shields.io/codecov/c/github/joshtemple/lkml.svg)](https://codecov.io/gh/jmbrooks/dbtea)
[![License](https://img.shields.io/github/license/jmbrooks/dbtea)](https://github.com/jmbrooks/dbtea/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# dbtea

Make more time for tea by teeing up with dbtea for dbt! :D

(Name definitely subject to change)

## Progress Note

This project is currently a work in progress in an alpha state. Its suite of use cases,
functionality, installation process, and details on how to use it will be documented here once
the project's features, process and code has reached a more stable state.

Generally speaking, is meant to make dbt project management easier: including but not limited
to:
 1) Generate dbt source and model YAML files in bulk, including incrementally adding to existing
 YAML files based on changes in source data and/or models.
 2) Passing metadata from dbt to downstream tools. In particular, taking dbtea descriptions, tags
 and meta properties and passing them to Looker as LookML descriptions and properties.
 3) Open pull requests against dbt or BI tool projects programmatically
