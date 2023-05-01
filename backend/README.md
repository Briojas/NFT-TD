# Django Server

## Setup

start pipenv virtual environment and install requirements

```
pipenv install
pipenv install -r requirements.txt
```

Check installation:

```
pipenv run python -m django --version
pipenv run python manage.py runserver
```

## Project Files and Usage

### /settings.py - list of configurations

- default database uses sqlite3
- add new apps to the project by:
  ```python
  INSTALLED_APPS = [
      "app_name.apps.AppConfig",
      "django.contrib.admin",
      "django.contrib.auth",
      "django.contrib.contenttypes",
      "django.contrib.sessions",
      "django.contrib.messages",
      "django.contrib.staticfiles",
  ]
  ```
  - where "app_name.apps.AppConfig" links to an app's "apps.py" file and the relevant object within

### /urls.py - "table of contents" for the Django-pwered site

- example:

  ```python
  from django.contrib import admin
  from django.urls import include, path

  urlpatterns = [
      path("app_url/", include("app_name.urls")),
      path("admin/", admin.site.urls),
  ]
  ```

- where:
  - "app_url/" is the index a user will route to on the site
  - the include("\*.urls") links to an app's urls.py file

### manage.py - cli tool

```
pipenv run python manage.py ...
```

- launch server:

  ```
  ... runserver
  ```

- create new app:

  ```
  ... startapp app_name
  ```

- build database tables:

  ```
  ... migrate
  ```

- store migrations of updated models:

  ```
  ... makemigrations app_name
  ```

  - rebuild database tables after makemigrations with "migrate"

- create admin user

  ```
  ... createsuperuser
  ```

- running tests for an app

```
''' test app_name
```

- tests are stored in the tests.py file of an app's folder

## App Files and Usage

### /views.py - html page to display when routed from a URL

- example:

  ```python
  from django.http import HttpResponse


  def index(request):
      return HttpResponse("Hello, world. You're at the url_here index.")
  ```

### /urls.py - (user-generated) indexes app views to URL routes

- example:

  ```python
  from django.urls import path

  from . import views

  urlpatterns = [
      path("", views.index, name="index"),
  ]
  ```

- where path(route, view, kwargs, name) params are defined as:
  - route: string for the URL route
  - view: function within views.py to call for returning a page
  - kwargs: dictionary of arguments to be passed to the views function
  - name: global reference for this url pattern

### /models.py - defines a database layout

- voting example:

  ```python
  from django.db import models

  class Question(models.Model):
      question_text = models.CharField(max_length=200)
      pub_date = models.DateTimeField("date published")

  class Choice(models.Model):
      question = models.ForeignKey(Question, on_delete=models.CASCADE)
      choice_text = models.CharField(max_length=200)
      votes = models.IntegerField(default=0)

  ```

  - where each Choice object contains a Question object

### /admin.py - registers objects to the admin interface

- example:

```python
from django.contrib import admin

from .models import DataObject

admin.site.register(DataObject)
```