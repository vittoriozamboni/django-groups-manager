Tests
=====

First of all, you need to clone the repository and create a virtualenv with all dependencies. Then you can run tests through the `manage.py` test command::

    virtualenv django-groups-manager-test
    cd django-groups-manager-test
    source bin/activate
    git clone https://github.com/vittoriozamboni/django-groups-manager.git
    cd django-groups-manager/testproject
    pip install -r requirements.txt
    python manage.py test testproject groups_manager

