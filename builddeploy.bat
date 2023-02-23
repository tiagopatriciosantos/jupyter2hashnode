call .\.venv\Scripts\activate
:: if prerelease run this instead of path-> call poetry version prerelease
:: call poetry version patch
:: we need to have set this variable # $ENV:POETRY_PYPI_TOKEN="pypi-
call poetry version patch
call poetry build
call poetry publish -u __token__ --password %POETRY_PYPI_TOKEN%

