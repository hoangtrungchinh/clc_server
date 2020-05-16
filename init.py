# Clean current migrations
import os

os.system('python3 manage.py migrate --fake cat zero')
os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
os.system('find . -path "*/migrations/*.pyc"  -delete ')

# Remove and create DB in Postgres
# https://pypi.org/project/django-postgres-dropdb/
# https://pypi.org/project/django-postgres-createdb/
os.system('python3 manage.py dropdb')
os.system('python3 manage.py createdb')

# migrate DB
os.system('python3 manage.py makemigrations')
os.system('python3 manage.py migrate')

# Load init Data
os.system('python3 manage.py loaddata initial_1k_data.yaml')
os.system('python3 manage.py search_index --rebuild')