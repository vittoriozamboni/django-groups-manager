# Django groups manager

[![Build Status](https://travis-ci.org/vittoriozamboni/django-groups-manager.svg?branch=master)](https://travis-ci.org/vittoriozamboni/django-groups-manager) [![Coverage Status](https://coveralls.io/repos/vittoriozamboni/django-groups-manager/badge.png?branch=master)](https://coveralls.io/r/vittoriozamboni/django-groups-manager?branch=master) ![Version](https://badge.fury.io/py/django-groups-manager.svg)

This application allows to create hierarchical groups by using [django-mptt](https://github.com/django-mptt/django-mptt) tree structure.
It is also possible to synchronize the groups with Django's ``auth.models`` Group and User, in order to take advantage of permissions applications like [django-guardian](https://github.com/lukaszb/django-guardian/).

## Documentation

Online documentation is available at http://django-groups-manager.rtfd.org/.

## Requirements

    - Django >= 1.7
    - django-guardian for user permissions (<1.4 for Django < 1.8)

## Installation

Use pip to install ``django-groups-manager``:

```bash
pip install django-groups-manager
```

### Django Configuration

1. Add ``groups_manager`` into your ``INSTALLED_APPS``:

    ```python
    INSTALLED_APPS = (
       ...
       'groups_manager',
    )
    ```

 If you want to use permissions related features, add also ``django-guardian``.

2. Create models with ``migrate``:

    ```bash
    python manage.py migrate groups_manager
    ```

    Note: for users that are upgrading from <0.4.2, launch:

    ```bash
    python manage.py migrate groups_manager 0001 --fake
    python manage.py migrate groups_manager
    ```

3. To enable django ``auth.models`` synchronization, add to the settings module:

    ```python
    GROUPS_MANAGER = {
        'DJANGO_AUTH_SYNC': True,
    }
    ```

## Basic usage

The common case is to create a simple parent-son relation:

```python
from groups_manager.models import Group, Member
fc_internazionale = Group.objects.create(name='F.C. Internazionale Milan')
staff = Group.objects.create(name='Staff', parent=fc_internazionale)
players = Group.objects.create(name='Players', parent=fc_internazionale)
thohir = Member.objects.create(first_name='Eric', last_name='Thohir')
staff.add_member(thohir)
palacio = Member.objects.create(first_name='Rodrigo', last_name='Palacio')
players.add_member(palacio)
```

Per-object permissions handling is done by ``django-guardian``. The Group/Member relation can be used to assing objects:

```python
from football.models import TeamBudget
small_budget = TeamBudget.objects.create(euros='1000')
thohir.assign_object(staff, small_budget)
thohir.has_perm('change_teambudget', small_budget)  # True
palacio.has_perm('change_teambudget', small_budget)  # False
# or via group
mid_budget = TeamBudget.objects.create(euros='3000')
staff.assign_object(mid_budget)
thohir.has_perm('change_teambudget', mid_budget)  # True
palacio.has_perm('change_teambudget', mid_budget)  # False
```

Owner/Group members policies can be defined via ``PERMISSIONS`` setting, as a dictionary of ``GROUPS_MANAGER``, but can also be overwritten via ``custom_permissions`` ``kwarg``:

```python
from football.models import Match
fc_barcelona = Group.objects.create(name='FC Barcelona')
friendly_match = Match.objects.create(home=fc_internazionale, away=fc_barcelona)
palacio.assign_match(players, friendly_match, custom_permissions={'group': ['play']})
thohir.has_perm('play_match', friendly_match)  # False
palacio.has_perm('play_match', friendly_match)  # True
```

For more complex cases, see documentation.
