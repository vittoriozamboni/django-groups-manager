import os
from setuptools import setup

try:
    import jsonfield
    _HAD_JSONFIELD = True
except ImportError:
    _HAD_JSONFIELD = False

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from groups_manager import VERSION

install_requires=[
    'awesome-slugify',
    'django>=2',
    'django-mptt',
]

if not _HAD_JSONFIELD:
    install_requires.append('jsonfield2')

setup(
    name='django-groups-manager',
    version=VERSION,
    description="Django groups manager through django-mptt.",
    long_description=README,
    long_description_content_type="text/markdown",
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
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Security',
    ],
)
