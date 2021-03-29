# Cars Rest Api

Rest Api for rating cars.

## Installation

Clone the repository to your local environment.
Set environment variables:
- SECRET_KEY
- DEBUG = 1  # if needed
- DATABASE_URL # if not set the default sqlite db will be used

Afterwards run:

python manage.py migrate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


## Problems with Heroku
There were some problems with deployment to heroku,
some errors occur when trying to make migrations. 

Here is a version that works, but not fully (apart from Popular endpoint).
I was trying different solutions but nothing works, yet on local machine everything works as it should.
https://fixing-example-245235346.herokuapp.com/
