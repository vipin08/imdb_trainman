## API Doc.

```
https://documenter.getpostman.com/view/1019794/TVCiUmiL
```

## Requirements

```
1. Python > 3.2
2. Django ~> 3.1
3. Rebbitmq
4. Redis Cache
```

## Instructions

create virtual env and activate env.

```
python3 -m venv venv && source venv/bin/activate
```

Install Dependencies

```
pip install -r requirements.txt
```

django maigrate file to db.

```
python manage.py migrate 
```

django create superuser

```
python manage.py createsuperuser
```

django server start at 8000 port

```
python manage.py runserver
```

Before start celery scheduler, make sure redis and rebbitmq is running on background.

```
celery worker --app movies_scrapper.celery.app
```