# mezzanine-openshift

This project is to provide the simplest way possible to run mezzanine on the
openshift stack with the best possible defaults for development and production.

#mezzanine-openshift 3.1

I've just updated the version of Django and Mezzanine, can change the python version too. Updated to:

Django==1.6.4
mezzanine==3.1.3

Changed basic configuration files too. 

* Thought wsgy.py in root isn't necessary
* Thought local_setting.py isn't necessary since exists settings folder

## Getting up and running

**NOTE**: Taken directly from the django-example by OpenShift.

Create an account at http://openshift.redhat.com/

Install the RHC client tools if you have not already done so:
    
    sudo gem install rhc

Create a python-2.6 application

    rhc app create -a mezzanine -t python-2.6

Add this upstream repo

    cd mezzanine
    git remote add upstream -m master git://github.com/overshard/mezzanine-openshift.git
    git pull -s recursive -X theirs upstream master

Then push the repo upstream

    git push

You can then access your new mezzanine instance at
http://mezzanine-$yournamespace.rhcloud.com with the username and password
`admin` and `default` respectively.


## Final notes

In `wsgi/openshift/settings/production.py` `DEBUG` is set to `True` in order to
get a default username and password but also for testing your app. Once you
actually go into production be sure to set this to `False`.
