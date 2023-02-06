call .\.venv\Scripts\activate
call poetry version patch
call poetry build
call poetry publish