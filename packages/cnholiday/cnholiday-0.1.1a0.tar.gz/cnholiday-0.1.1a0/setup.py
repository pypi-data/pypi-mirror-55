# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cnholiday']

package_data = \
{'': ['*']}

install_requires = \
['pre-commit>=1.20,<2.0']

entry_points = \
{'console_scripts': ['app = cnholiday:app']}

setup_kwargs = {
    'name': 'cnholiday',
    'version': '0.1.1a0',
    'description': '查询某天是否放假',
    'long_description': '# CNHoliday: 查询某天是否放假\n\n数据来源: <http://www.gov.cn/zhengce/content/2018-12/06/content_5346276.htm>\n\n用法：\n\n```python\nfrom cnholiday import CNHoliday\n\n\ncnholiday = CNHoliday()\n_day = datetime(2019, 10, 1)\nprint(cnholiday.check(_day))\nprint(cnholiday.check_shift(_day))\nprint(cnholiday.check_shift(_day, shift=2))\nprint(cnholiday.check_shift(_day, shift=3))\n```\n',
    'author': 'ringsaturn',
    'author_email': 'ringsaturn.me@gmail.com',
    'url': 'https://github.com/ringsaturn/cnholiday',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
