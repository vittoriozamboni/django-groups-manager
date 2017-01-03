Templates
=========

Requirements
^^^^^^^^^^^^

The supported templates requires bootstrap3. Forms are based on ``django-bootstrap3`` application, that can be installed with::

    pip install django-bootstrap3

This application is used only to render forms.
If you don't want to use it's default rendering, you can override the ``form_template.html`` file as described in the example below.

Structure
^^^^^^^^^

Templates are organized in different sections, inside ``groups_manager/bootstrap3`` folder.::

    - groups_manager.html (extends "base.html")
      | - groups_manager_home.html (menu with links to models lists)
      | - <model>.html (model base, i.e. "member", extended by all model templates)
          | - <model>_list.html
          | - <model>_detail.html
          | - <model>_form.html (includes form_template.html)
          | - <model>_confirm_delete.html

There are different blocks:

    - ``breadcrumbs``: usually displayed on top of the page, with ``app - model - page`` links
    - ``sidebar``: menu available for the application and <model> actions (add, edit, etc)
    - ``content``: the main content of the page

To change a template, creates the same structure inside an application loaded after ``groups_manager``
in your ``INSTALLED_APPS``.
For example, to change ``form_template.html`` file, create the folders "groups_manager/bootstrap3/" and put
the file "form_template.html" inside.

Style
^^^^^

By default, style is "bootstrap3": this means that templates are searched inside folder "groups_manager/bootstrap3".
To change this behaviour, edit setting ``TEMPLATE_STYLE``: it will be used in the views::

    template_name = 'groups_manager%s/groups_manager.html' % TS
