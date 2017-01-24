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

To start your postgres database
```{r, engine='bash', count_lines}
createdb <database name>
export IMAGER_DATABASE="<database name>"
export TEST_IMAGER="test"
```
or

In **/django-imager/imagersite/imagersite/settings.py** on line 80 replace:
```python
'NAME': os.environ['IMAGER_DATABASE'],
```
with 
```python
'NAME': <database name>,
```