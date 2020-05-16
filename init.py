# Clean current migrations
import os
import subprocess

os.system('python3 manage.py migrate --fake cat zero')
os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
os.system('find . -path "*/migrations/*.pyc"  -delete ')

print("\n====== Remove and create DB in Postgres ====== ")
# https://pypi.org/project/django-postgres-dropdb/
# https://pypi.org/project/django-postgres-createdb/
os.system('python3 manage.py dropdb')
os.system('python3 manage.py createdb')

print("\n====== migrate DB ====== ")
os.system('python3 manage.py makemigrations')
os.system('python3 manage.py migrate')


print("\n====== Load init Data ====== ")
os.system('python3 manage.py loaddata initial_1k_data.yaml')


print("\n====== Rebuild in Elastic Search ====== ")
subprocess.Popen(['echo Y | python3 manage.py search_index --rebuild'], shell=True)

print("\n====== Proceess Complete ====== ")
