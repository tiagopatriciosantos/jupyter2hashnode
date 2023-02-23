call .\.venv\Scripts\activate
call poetry config repositories.%POETRY_TESTPY_REP% https://test.pypi.org/legacy/
call poetry config pypi-token.%POETRY_TESTPY_REP%  %POETRY_TESTPY_TOKEN%
:: if prerelease run this instead of path-> call poetry version prerelease
:: # $ENV:POETRY_TESTPY_REP="testpypi"
:: # $ENV:POETRY_TESTPY_TOKEN="pypi-
call poetry version patch
call poetry build
call poetry publish -r testpypi