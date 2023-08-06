# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tips', 'tips.migrations']

package_data = \
{'': ['*'], 'tips': ['static/tips/js/*', 'templates/tips/*']}

install_requires = \
['django>=2.0,<3.0', 'djangorestframework>=3.10', 'markdown>=2.6']

setup_kwargs = {
    'name': 'django-tips',
    'version': '0.8.2',
    'description': 'Show tip of the day cards on your site.',
    'long_description': '=============================\ndjango-tips\n=============================\n\n.. image:: https://badge.fury.io/py/django-tips.png\n    :target: https://badge.fury.io/py/django-tips\n\n.. image:: https://travis-ci.org/trojsten/django-tips.png?branch=master\n    :target: https://travis-ci.org/trojsten/django-tips\n\nShow tip of the day cards on your site.\n\nQuickstart\n----------\n\nInstall django-tips::\n\n    pip install django-tips\n\nThen use it in a project::\n\n    import tips\n\nRequirements\n------------\n\n* django\n* djangorestframework\n* markdown\n\nRecommanded packages\n--------------------\n\n* django-sekizai\n\nBuilding frontend\n-----------------\n\nFrom tips_frontend directory run::\n\n    npm run dev\n\nor production build::\n\n    npm run build\n\nUsage\n-----\nplace where you want to show tips::\n\n    {% include "tips/tips.html" %}\n\ninclude csrf-token ajax setup script if you have csrf protection enabled (you can find the script in the example)::\n\n    <script src="{% static "js/csrf_token.js" %}"></script>\n\nDevelopment\n-----------\n::\n\n    pip install poetry\n    poetry install\n    cd example\n    ./manage.py migrate\n    ./manage.py loaddata fixtures/initial_data.json\n    ./manage.py createsuperuser\n    ./manage.py runserver\n\nCredits\n-------\n\nTools used in rendering this package:\n\n*  Cookiecutter_\n*  `cookiecutter-djangopackage`_\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`cookiecutter-djangopackage`: https://github.com/trojsten/cookiecutter-djangopackage\n',
    'author': 'Michal Hozza',
    'author_email': 'mhozza@gmail.com',
    'url': 'https://github.com/trojsten/django-tips',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
