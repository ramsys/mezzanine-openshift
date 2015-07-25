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
    python manage.py createdb --settings=settings.production

## Connect to OpenShift PostgreSQL

Run port-forwarding to application

    rhc port-forward mezzanine

And then configure new connection pgAdmin

# Amazon S3

Create bucket in Amazon S3 and add policy. Refer:

  https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/

Download libraries for talk with S3

    pip install django-storages boto

Add to INSTALLED_APPS

    INSTALLED_APPS = (
          ...,
          'storages',
     )

Add cache headers, for performance

```python
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
  'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
  'Cache-Control': 'max-age=94608000',
}
```

Add S3 configuration to settings.py

```python
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
```

Add Openshift environment variables

     rhc env set AWS_STORAGE_BUCKET_NAME='<value>'
     rhc env set AWS_ACCESS_KEY_ID='<value>'
     rhc env set AWS_SECRET_ACCESS_KEY='<value>'

Finally, connect to Openshift SSH and execute collectstatic

    source $OPENSHIFT_HOMEDIR/python/virtenv/bin/activate
    cd $OPENSHIFT_REPO_DIR/wsgi/$OPENSHIFT_APP_NAME
    python manage.py collectstatic --settings=settings.production

Reference: https://developers.openshift.com/en/managing-environment-variables.html#custom-variables


## Final notes

In `wsgi/openshift/settings/production.py` `DEBUG` is set to `True` in order to
get a default username and password but also for testing your app. Once you
actually go into production be sure to set this to `False`.
