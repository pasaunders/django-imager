[![Build Status](https://travis-ci.org/pasaunders/django-imager.svg?branch=deployment)](https://travis-ci.org/pasaunders/django-imager)
# Django-Imager
An image display app built in django as a learning project

Creators:

Amos Bolder, Patrick Saunders

URL: http://ec2-54-202-239-113.us-west-2.compute.amazonaws.com/


##Getting Started

Clone this repository into whatever directory you want to work from.
```
https://github.com/pasaunders/django-imager.git
```
Assuming that you have access to Python 3 at the system level, start up a new virtual environment.
```
$ cd django-imager
$ python3 -m venv ENV
$ source ENV/bin/activate
```
Once your environment has been activated, make sure to install Django and all of this project's required packages.
```
$ pip install -r requirements.pip
```
Navigate to the project root, imagersite, and apply the migrations for the app.
```
$ cd imagersite

$ ./manage.py migrate
```
Finally, run the server in order to server the app on localhost
```
$ ./manage.py runserver
```
Django will typically serve on port 8000, unless you specify otherwise. You can access the locally-served site at the address http://localhost:8000.


##Current Models (outside of Django built-ins):

This application allow users to store and organize photos.

**The `ImagerProfile` model contains:**

- Address
- Bio
- Personal website
- Whether the user is for hire
- Distance the user is willing to travel for work
- Phone contact
- User's preferred style of photography
- The model manager has been edited to provide a list of active users

**The `Photo` model contains:**

- The Image
- Image title
- A description of the image
- Records of the dates when the image was uploaded, last modified, and published.
- Whether the image is public, private or shared
Photos are associated with users in a many-to-one relationship

**The `Album` model contains:**

- An album cover image
- Album title
- A description of the album
- Date the album was created, modified and published
- Whether the album is public, private or shared
Albums are associated with users in a many-to-one relationship
Albums are associated with photos in a many-to-many relationship

##Current URL Routes

- `/admin` Superuser admin page
- `/` Home page
- `/login` Login page
- `/logout` Logout route, no view
- `/accounts/register` Register a user form
- `/accounts/activate/complete/` Activation complete view
- `/accounts/register/complete/` Registration complete, email sent
- `/profile/` Authenticated user's profile view
- `/profile/edit/` Profile edit view
- `/profile/<username>/` Profile view for named user
- `/images/photos/add/` Add a photo
- `/images/<photo_id>/` View a single photo
- `/images/<photo_id>/edit` Edit a photo
- `/images/photos/` View all of an authenticated user's authorized photos
- `/images/albums/<album_id>/` View a particular album
- `/images/albums/<album_id>/edit` Edit an album
- `/images/albums/add/` Add an album
- `/images/albums/` View all authorized volumes
- `/images/library/` View authenticated user's library
- `/images/tagged/<slug>/` View photos with a tag
- `/api/v1/` Api access
- `/oauth/` Social django package


##Running Tests

Running tests for the django-imager is fairly straightforward. Navigate to the same directory as the manage.py file and type:
```
$ coverage run manage.py test
```
This will show you which tests have failed, which tests have passed. If you'd like a report of the actual coverage of your tests, type
```
$ coverage report
```
This will read from the included .coverage file, with configuration set in the .coveragerc file. Currently the configuration will show which lines were missing from the test coverage.
