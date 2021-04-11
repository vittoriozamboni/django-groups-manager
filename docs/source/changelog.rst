Changelog
=========
- 21-04-11 (1.1.0):
    - Removed `awesome-slugify` from requirements. It needs to be installed separately due to his licence (see issue #54, thank you BoPeng!);
    - Added a new settings to customize the slugify functions for username and other cases.

- 20-06-17 (1.0.2):
    - Changed jsonfield2 to jsonfield in requirements

- 20-03-07 (1.0.1):
    - Amended Django 3 deprecations
    - Documentation changes

- 19-12-10 (1.0.0):
    - Dropped support for Django < 2 and Python 2.*

- 19-01-11 (0.6.2):
    - Added migrations for expiration_date and verbose names

- 18-01-18 (0.6.1):
    - Added support for Django 2

- 17-12-09 (0.6.0) (thank you Oskar Persson!):
    - Added group type permission handling
    - Added ``expiration_date`` attribute
    - Added support to django-jsonfield

- 16-11-08 (0.5.0):
    - Added models mixins
    - Removed compatibility for Django < 1.7

- 16-10-10 (0.4.2):
    - Added initial migration
    - Removed null attributes from m2m relations

- 16-04-19 (0.4.1):
    - Removed unique to group name (this cause issues when subclassing, since it does not allows to have same names for different models)
    - Fixed issue with python 3 compatibility in templatetags (thank you Josh Manning!)

- 16-03-01 (0.4.0):
    - Added kwargs to signals for override settings parameters
    - Added remove_member to group as a method (previously must be done manually)

- 16-02-25 (0.3.0):
    - Added permissions assignment to groups
    - Added support for Django 1.8 and 1.9

- 15-05-05 (0.2.1):
    - Added 'add' to default permissions

- 15-05-05 (0.2.0):
    - Changed retrieval of permission's name: 'view', 'change' and 'delete' will be translated to '<name>_<model_name>', the others are left untouched (see :ref:`permission name policy <permission-name-policy>`)
    - Added GroupsManagerMeta class to Group that allows to specify the member model to use for members list (see :ref:`custom Member model <custom-member-model>`)

- 14-10-29 (0.1.0): Initial version
