# Releasing a new version of dbtea

## Follow semver

Dbtea follows semantic versioning. Familiarize yourself with [semver](https://semver.org/) before creating a new
version of dbtea. Non-development releases should be approved by the project maintainers.

## Write a draft release on GitHub

*Doesn't apply to development versions (alpha, beta, or release candidate)*

1. The release notes should have two sections: **Features** for new functionality and **Fixes** for bugfixes or internal changes.

1. Include links for each feature or fix to any relevant GitHub issues or documentation sections. See [previous releases](https://github.com/4mile/dbtea/releases/tag/v0.1.0) for examples.

1. Save the release as a draft. If you'd like, you can draft and edit the release notes as you merge features and fixes, it's not public.

## Get code and docs ready

All code to be released should be merged into `main`. If the release is a major or minor release, there should be a corresponding, approved PR on the docs repository ready to be merged that covers any notable new functionality or API changes.

## Bump the version

The version number for dbtea is stored in the `__init__.py` file in `dbtea/` as the argument `__version__`.

Change the version there and commit it with the message "Bump version [CURRENT_VERSION] > [NEW_VERSION]". You can commit this directly to `main` or create a separate branch (e.g. `release/0.2.2`) for this change.

## Build distributions

To build distributions, run the following command from the root of the dbtea repository on the `main
` branch.

```bash
python setup.py sdist bdist_wheel
```

This command will build distributions in the `dist` directory within the dbtea repository root.

## Deploy to PyPi

To deploy a release, you must have an account on PyPi with at least Maintainer role on the [dbtea project](https://pypi.org/manage/project/dbtea/collaboration/).

Next, install [`twine`](https://twine.readthedocs.io/en/latest/#installation) and optionally [set up Keyring](https://twine.readthedocs.io/en/latest/#keyring-support) so you don't have to enter your username and password each time.

To deploy to production PyPi, use this command:
```bash
twine upload --skip-existing dist/*
```

To deploy to the test PyPi instance, use this command instead:
```bash
twine upload --skip-existing --repository testpypi dist/*
```

## Publish draft GitHub release

*Doesn't apply to development versions (alpha, beta, or release candidate)*

Publish the draft release. This will generate a corresponding tag on the HEAD commit of `main`.

## Merge the docs PR and announce

*Doesn't apply to development versions (alpha, beta, or release candidate)*

At this point, the release is ready to share with the world. Merge any corresponding docs PR and announce the release in the dbt Slack!