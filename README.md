Solution comprises several services:
1. web-scraper - a web-application that authentificate the user and show him news.
   # cmd
   # D:
   # cd "D:\КУРС Python\Graduation_project"
   # # mkdir web_scraper
   # cd web_scraper
   # # pipenv install requests bs4 lxml django celery gevent
   # # django-admin startproject web_scraper .
   # # python manage.py createsuperuser
   # # python manage.py makemigrations
   # # python manage.py migrate
   # python manage.py runserver
2. scraping - a scraping application that defines the data model and collects the data.
   # # python manage.py startapp scraping
   # # python manage.py makemigrations
   # # python manage.py migrate
3. celery - a standard task queue implementation for Python web applications used to asynchronously execute "news scraping" tasks according to a defined schedule.
   # cmd
   # D:
   # cd "D:\КУРС Python\Graduation_project\web_scraper"
   # celery -A web_scraper.celery worker -l INFO -P gevent
   # cmd 
   # D:
   # cd "D:\КУРС Python\Graduation_project\web_scraper"
   # celery -A web_scraper beat -l INFO
4. RabbitMQ - a message broker used by celery.
   # cmd
   # cd "C:\Program Files\RabbitMQ Server\rabbitmq_server-3.12.2\sbin"
   # rabbitmqctl stop
   # rabbitmq-server
