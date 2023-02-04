call .\.venv\Scripts\activate
call python -m build
call py -m twine upload --skip-existing dist/*