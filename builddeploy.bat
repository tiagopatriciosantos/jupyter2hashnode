call .\.venv\Scripts\activate
call python -m build
call py -m twine upload dist/*