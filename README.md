[![Build Status](https://travis-ci.org/pasaunders/django-imager.svg?branch=master)](https://travis-ci.org/pasaunders/django-imager)
# Django-Imager
## Getting Started

Clone this repository into whatever directory you want to work from.

```bash
$ git clone https://github.com/pasaunders/django-imager.git
```

Assuming that you have access to Python 3 at the system level, start up a new virtual environment.

```bash
$ cd django-imager
$ python3 -m venv .
$ source bin/activate
```

Once your environment has been activated, make sure to install Django and all of this project's required packages.

```bash
(django-imager) $ pip install -r requirements.pip
```

Navigate to the project root, `imagersite`, and apply the migrations for the app.

```bash
(django-imager) $ cd lending_library
(django-imager) $ ./manage.py migrate
```

Finally, run the server in order to server the app on `localhost`

```bash
(django-imager) $ ./manage.py runserver
```

Django will typically serve on port 8000, unless you specify otherwise.
You can access the locally-served site at the address `http://localhost:8000`.