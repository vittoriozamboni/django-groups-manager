import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from groups_manager import VERSION

setup(
    name='django-groups-manager',
    version=VERSION,
    description="Django groups manager through django-mptt.",
    long_description=README,
    author='Vittorio Zamboni',
    author_email='vittorio.zamboni@gmail.com',
    license='MIT',
    url='https://github.com/vittoriozamboni/django-groups-manager',
    packages=[
        'groups_manager',
        'groups_manager.migrations',
        'groups_manager.templatetags',
    ],
    include_package_data=True,
    install_requires=[
        'awesome-slugify',
        'django>=1.7',
        'django-braces',
        'django-guardian',
        'django-mptt',
        'jsonfield',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Security',
    ],
)
