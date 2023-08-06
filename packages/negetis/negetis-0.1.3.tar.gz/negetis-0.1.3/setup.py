# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['negetis']

package_data = \
{'': ['*'],
 'negetis': ['resources/example/*',
             'resources/example/content/en/*',
             'resources/example/content/en/about/*',
             'resources/example/content/en/about/company/*',
             'resources/example/content/en/posts/*',
             'resources/example/content/rus/*',
             'resources/example/content/rus/about/*',
             'resources/example/static/en/*',
             'resources/example/static/ru/*',
             'resources/example/themes/basic/*',
             'resources/example/themes/basic/archetypes/*',
             'resources/example/themes/basic/layouts/*',
             'resources/example/themes/basic/layouts/partials/*',
             'resources/example/themes/basic/static/img/*',
             'resources/i18n/*',
             'resources/site/*',
             'resources/site/content/*',
             'resources/site/static/*',
             'resources/site/themes/*',
             'resources/theme/*',
             'resources/theme/archetypes/*',
             'resources/theme/layouts/*',
             'resources/theme/layouts/_base/*',
             'resources/theme/layouts/partials/*',
             'resources/theme/static/css/*',
             'resources/theme/static/js/*']}

install_requires = \
['Click>=7.0,<8.0',
 'asq>=1.3,<2.0',
 'deepmerge>=0.1.0,<0.2.0',
 'deprecation>=2.0,<3.0',
 'jinja2>=2.10,<3.0',
 'markdown>=3.1,<4.0',
 'pillow>=6.2,<7.0',
 'python-i18n[YAML]>=0.3.7,<0.4.0',
 'python-thumbnails>=0.5.1,<0.6.0',
 'pytz>=2019.3,<2020.0',
 'pyyaml-include>=1.1,<2.0',
 'pyyaml>=5.1,<6.0',
 'watchdog>=0.9.0,<0.10.0',
 'werkzeug>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['negetis = negetis.main:run']}

setup_kwargs = {
    'name': 'negetis',
    'version': '0.1.3',
    'description': 'Static site generator',
    'long_description': 'neGetiS\n=======\n\nStatic site generator\n\n\nInstalation\n-----------\n\n```\npip install negetis \n```\n\nUsage\n-----\n\n```\nnegetis newsite my-first-site\ncd ./my-first-site\nnegetis addtheme basic\nnegetis post my-first-post\nnano ./content/posts/my-first-post.md\nnegetis server -D\n```\n\nopen browser at `http://localhost:8888/`\n\n\n\nDevelop\n-------\n\nRequirements:\n\n* poetry\n\n\n```\ngit clone https://github.com/AxGrid/neGetiS.git\ncd ./neGetiS\npoetry install\n```',
    'author': 'Dmitry Vysochin',
    'author_email': 'dmitry.vysochin@gmail.com',
    'url': 'http://negetis.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
