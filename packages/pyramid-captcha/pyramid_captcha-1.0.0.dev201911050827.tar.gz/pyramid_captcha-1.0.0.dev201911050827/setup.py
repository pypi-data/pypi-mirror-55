import codecs
import os
import sys
from datetime import datetime

from setuptools import setup, find_packages

VERSION = '1.0.0'

requires = [
    'pyramid',
    'pyramid_beaker',
    'captcha',
    'waitress'
]

dev = False
timestamp = datetime.now().strftime('%Y%m%d%H%M')

if "--dev" in sys.argv:
    dev = True
    sys.argv.remove('--dev')

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    description = f.read()

with codecs.open(os.path.join(here, 'CHANGELOG.rst'), encoding='utf-8') as f:
    description += '\n\n'
    description += f.read()


setup(
    name='pyramid_captcha',
    version=VERSION + '-dev.{0}'.format(timestamp) if dev else VERSION,
    description='Pyramid Captcha',
    long_description=description,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 4 - Beta' if dev else 'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP'
    ],
    author='Karsten Deininger',
    author_email='karsten.deininger@bl.ch',
    url='https://gitlab.com/geo-bl-ch/pyramid-captcha',
    keywords='web pyramid captcha',
    install_requires=requires,
    packages=find_packages(exclude=['demo', 'test*']),
    include_package_data=True
)
