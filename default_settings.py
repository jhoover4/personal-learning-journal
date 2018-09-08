import os

is_prod = os.environ.get('HEROKU', None)

if is_prod:
    DEBUG = os.environ.get('DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY')
else:
    DEBUG = True
    SECRET_KEY = 'ASDF!@#$5%$@#$%fasdf'
