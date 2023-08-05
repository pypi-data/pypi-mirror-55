# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bareasgi_jinja2']

package_data = \
{'': ['*']}

install_requires = \
['bareasgi>=3.3,<4.0', 'jinja2>=2.10,<3.0']

setup_kwargs = {
    'name': 'bareasgi-jinja2',
    'version': '3.1.1',
    'description': 'Jinja2 support for bareasgi',
    'long_description': "# bareASGI-jinja2\n\nJinja2 support for [bareASGI](http://github.com/rob-blackbourn/bareasgi) (read the [documentation](https://bareasgi-jinja2.readthedocs.io/en/latest/))\n\n## Usage\n\nTry the following.\n\n```python\nfrom typing import Mapping, Any\nimport jinja2\nimport os.path\nimport uvicorn\nfrom bareasgi import Application\nimport bareasgi_jinja2\n\nhere = os.path.abspath(os.path.dirname(__file__))\n\n@bareasgi_jinja2.template('example1.html')\nasync def http_request_handler(scope, info, matches, content):\n    return {'name': 'rob'}\n\napp = Application()\n\nenv = jinja2.Environment(\n    loader=jinja2.FileSystemLoader(os.path.join(here, 'templates')),\n    autoescape=jinja2.select_autoescape(['html', 'xml']),\n    enable_async=True\n)\n\nbareasgi_jinja2.add_jinja2(app, env)\n\napp.http_router.add({'GET'}, '/example1', http_request_handler)\n\nuvicorn.run(app, port=9010)\n\n```\n",
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'url': 'https://github.com/rob-blackbourn/bareasgi-jinja2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
