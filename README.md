# mezzanine-openshift

This project is to provide the simplest way possible to run mezzanine on the
openshift stack with the best possible defaults for development and production.

## Current Mezzanine version

* 'Django==1.6.11'
* 'mezzanine==3.1.10'
* 'django_compressor==1.5'


# Local

## Quick start local application

Preparation local environment

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Creating a demo application

    python manage.py createdb --settings=settings.development
    ...

For execute local server

     python manage.py runserver --settings=settings.development

Open url http://127.0.0.1:8000

Start modifying application

    python manage.py collecttemplates --settings=settings.development

# OpenShift

## Getting up and running

**NOTE**: Taken directly from the django-example by OpenShift.

Create an account at http://openshift.redhat.com/

Install the RHC client tools if you have not already done so:

    sudo gem install rhc

Create a python-2.7 application

    rhc app create -a mezzanine -t python-2.7

Add this upstream repo

    cd mezzanine
    git remote add upstream -m master git://github.com/ramsys/mezzanine-openshift.git
    git pull -s recursive -X theirs upstream master


Then push the repo upstream

    git push

You can then access your new mezzanine instance at
http://mezzanine-$yournamespace.rhcloud.com with the username and password
`admin` and `default` respectively.

## Configuring PostgreSQL DB

Add to settings/production.py DATABASE configuration

```python
# a setting to determine whether we are running on OpenShift
ON_OPENSHIFT = False
EXISTS_POSTGRESQL = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True
if os.environ.has_key('OPENSHIFT_APP_NAME'):
    DB_NAME = os.environ['OPENSHIFT_APP_NAME']
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_USERNAME'):
    EXISTS_POSTGRESQL = True
    DB_USER = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_PASSWORD'):
    DB_PASSWD = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_HOST'):
    DB_HOST = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_PORT'):
    DB_PORT = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']


if EXISTS_POSTGRESQL:
    # os.environ['OPENSHIFT_DB_*'] variables can be used with databases created
    # with rhc app cartridge add (see /README in this git repo)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': DB_NAME,               # Or path to database file if using sqlite3.
            'USER': DB_USER,               # Not used with sqlite3.
            'PASSWORD': DB_PASSWD,         # Not used with sqlite3.
            'HOST': DB_HOST,               # Set to empty string for localhost. Not used with sqlite3.
            'PORT': DB_PORT,               # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'sqlite3.db'),
        }
    }

```

Connect ssh OPENSHIFT cartridge and run createdb

    source $OPENSHIFT_HOMEDIR/python-2.6/virtenv/bin/activate
    cd $OPENSHIFT_REPO_DIR/wsgi/$OPENSHIFT_APP_NAME
    # python manage.py syncdb
    python manage.py createdb

## Connect to OpenShift PostgreSQL

Run port-forwarding to application

    rhc port-forward mezzanine

And then configure new connection pgAdmin

## Final notes

In `wsgi/openshift/settings/production.py` `DEBUG` is set to `True` in order to
get a default username and password but also for testing your app. Once you
actually go into production be sure to set this to `False`.
