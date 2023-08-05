# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_model_subscription', 'model_subscription']

package_data = \
{'': ['*']}

install_requires = \
['django-lifecycle>=0.3.0,<0.4.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8" or python_version >= "3.4" and python_version < "3.5"': ['typing>=3.6,<4.0']}

setup_kwargs = {
    'name': 'django-model-subscription',
    'version': '0.0.6',
    'description': 'Subscription model for a django model instance.',
    'long_description': '# [django-model-subscription](https://django-model-subscription.readthedocs.io/en/latest/installation.html)\n[![Documentation Status](https://readthedocs.org/projects/django-model-subscription/badge/?version=latest)](https://django-model-subscription.readthedocs.io/en/latest/?badge=latest) [![CircleCI](https://circleci.com/gh/jackton1/django-model-subscription.svg?style=svg)](https://circleci.com/gh/jackton1/django-model-subscription)\n\nhttps://python-3-patterns-idioms-test.readthedocs.io/en/latest/Observer.html\n',
    'author': 'Tonye Jack',
    'author_email': 'tonyejck@gmail.com',
    'url': 'https://django-model-subscription.readthedocs.io/en/latest/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
