from distutils.core import setup

from groups_manager import VERSION

setup(
    name='django-groups-manager',
    version=VERSION,
    description="Django groups manager through django-mptt.",
    author='Vittorio Zamboni',
    author_email='vittorio.zamboni@gmail.com',
    license='MIT',
    url='http://bitbucket.org/zamboni/django-groups-manager',
    packages=[
        'groups_manager',
        'groups_manager.templatetags',
    ],
    install_requires=[
        'awesome-slugify',
        'django>=1.4',
        'django-braces',
        'django-mptt',
        'jsonfield',
    ],
)
