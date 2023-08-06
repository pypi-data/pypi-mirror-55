# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['calender', 'calender.migrations']

package_data = \
{'': ['*'], 'calender': ['templates/calender/*']}

install_requires = \
['django-environ>=0.4.5,<0.5.0',
 'django>=2.2,<3.0',
 'lxml>=4.4,<5.0',
 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['vote4film = manage:main']}

setup_kwargs = {
    'name': 'vote4film',
    'version': '1.0.1',
    'description': 'Easy scheduling for regular film nights',
    'long_description': '# Vote4Film\n\nSimplify film selection for regular film nights. Participants can:\n\n- Add films\n- Vote for films\n- Declare absences\n- See the schedule which takes into account votes and absences\n\nAdmins can set the schedule of film nights.\n\nThis is a simple WSGI Web Application.\n\n## Development\n\n1. `poetry install` to set-up the virtualenv (one-off)\n2. `poetry run ./src/vote4film/manage.py migrate` to set-up the local DB (one-off)\n3. `poetry run ./src/vote4film/manage.py runserver_plus`\n4. `make check` and `make test` before committing\n\n### Publishing\n\nThis application will be published on PyPi.\n\n1. Ensure you have configured Poetry repositories including `TestPyPi` (one-off)\n2. `poetry publish --build -r testpypi` to upload to the test repository\n3. `poetry publish --build` to release\n\n## Deployment\n\nUnfortunately, I will not provide any guidance here.\n\n## Changelog\n\n### v1.0.1 - 2019/11/10\n\n- First release of Vote4Film.\n',
    'author': 'QasimK',
    'author_email': 'noreply@QasimK.io',
    'url': 'https://github.com/Fustra/vote4film/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
