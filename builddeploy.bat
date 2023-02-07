call .\.venv\Scripts\activate
:: if prerelease run this instead of path-> call poetry version prerelease
:: call poetry version patch
call poetry version patch
call poetry build
call poetry publish -u __token__ --password %POETRY_PYPI_TOKEN%

