# django_sites

mysite - from Django tutorial (https://docs.djangoproject.com/en/1.9/intro etc.)

illumina_submission_py - to replace the old php version

START:
---
sudo pip install Django

django-admin startproject illumina_submission_py

mysql as root:

mysql> CREATE USER 'dj_admin'@'localhost';

mysql> GRANT ALL PRIVILEGES ON *.* TO 'dj_admin'@'localhost'

mysql> SET PASSWORD = PASSWORD('some_password');

mysql> create database dj_test;

mysql> flush privileges;

python manage.py runserver 0.0.0.0:8000

python manage.py migrate

python manage.py runserver


Put your code in some directory outside of the document root, such as /home/mycode.

Clean with 

mysite$ flake8 . | grep -v "line too long" > flake_res; mate flake_res
