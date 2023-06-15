Changelog
=========

- 2023-06-15 (1.3.0):
    - Verified compatibility with Django up to 4.2 and Python up to 3.11.
    - Dropped compatibility guarantees with anything older than Django 3.2 and Python 3.8.
    - Use Django's build in models.JSONField instead of the one from the jsonfield package.
    - Minor documentation changes

- 2022-01-29 (1.2.0):
    - Support Django 4: uses correct url parser function `re_path` (see issue #60, thank you Lukas Hennies!)
    - Updated intro.rst, fixed wrong example (see issue #57, thank you Areski Belaid!)

- 2021-04-11 (1.1.0):
    - Removed `awesome-slugify` from requirements. It needs to be installed separately due to his licence (see issue #54, thank you BoPeng!);
    - Added a new settings to customize the slugify functions for username and other cases.

- 2020-06-17 (1.0.2):
    - Changed jsonfield2 to jsonfield in requirements and tests (see issue #49, thank you ioio!);

- 2020-03-07 (1.0.1):
    - Amended Django 3 deprecations
    - Documentation changes

- 2019-12-10 (1.0.0):
    - Dropped support for Django < 2 and Python 2.*

- 2019-01-11 (0.6.2):
    - Added migrations for expiration_date and verbose names

- 2018-01-18 (0.6.1):
    - Added support for Django 2

- 2017-12-09 (0.6.0) (thank you Oskar Persson!):
    - Added group type permission handling
    - Added ``expiration_date`` attribute
    - Added support to django-jsonfield

- 2016-11-08 (0.5.0):
    - Added models mixins
    - Removed compatibility for Django < 1.7

- 2016-10-10 (0.4.2):
    - Added initial migration
    - Removed null attributes from m2m relations

- 2016-04-19 (0.4.1):
    - Removed unique to group name (this cause issues when subclassing, since it does not allows to have same names for different models)
    - Fixed issue with python 3 compatibility in templatetags (thank you Josh Manning!)

- 2016-03-01 (0.4.0):
    - Added kwargs to signals for override settings parameters
    - Added remove_member to group as a method (previously must be done manually)

- 2016-02-25 (0.3.0):
    - Added permissions assignment to groups
    - Added support for Django 1.8 and 1.9

- 2015-05-05 (0.2.1):
    - Added 'add' to default permissions

- 2015-05-05 (0.2.0):
    - Changed retrieval of permission's name: 'view', 'change' and 'delete' will be translated to '<name>_<model_name>', the others are left untouched (see :ref:`permission name policy <permission-name-policy>`)
    - Added GroupsManagerMeta class to Group that allows to specify the member model to use for members list (see `custom Member model <custom_member>`)

- 2014-10-29 (0.1.0): Initial version
