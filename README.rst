=============
pinax-tracker
=============

A pinax project expanding on the existing pinax features to make a more
complete issue tracker.

Right now the project adds milestones and a dashboard interface to the
existing pinax code_project.

This is currently an experiment to see what a tracker with pinax could look
like and is not intended to replace any of the exiting open source trackers.

I would like to borrow as much as possible from the excelent Basie project (http://basieproject.org/), which is a powerful Django port of trac.

Try the demo: http://pinax-tracker.hbussell.com

Login as demo / demo

This project is released under the MIT License.

------------
Installation
------------

Create a new virtual env ::

    mkdir pinax-tracker
    cd pinax-tracker
    virtualenv --no-site-packages env

Activate the virtual env ::    

    source env/bin/activate

Install pip ::

    easy_install pip

Clone the project into the website folder ::

    git clone git://github.com/hbussell/pinax-tracker.git website

Install requirements ::

    cd website
    pip install -r frozen.txt

Build app media into static_media ::

    python manage.py build_static

Now you can run syncdb and start the project ::

    python manage.py syncdb
    python manage.py runserver

Optionally install the sample data ::

    python manage.py loaddata sample_data.json


