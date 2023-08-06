# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['redis_index']

package_data = \
{'': ['*']}

install_requires = \
['hot_redis>=0.3.0,<0.4.0', 'inflection>=0.3.1,<0.4.0', 'statsd>=3.3,<4.0']

setup_kwargs = {
    'name': 'redis-index',
    'version': '0.1.11',
    'description': 'Inverted Index using efficient Redis set',
    'long_description': '# Redis-index: Inverted Index using efficient Redis set\n\nRedis-index helps to delegate part of the work from database to cache.\nIt is useful for highload projects, with complex serach logic underneath the hood.\n\n[![Build Status](https://github.com/ErhoSen/redis-index/workflows/Build/badge.svg)](https://github.com/ErhoSen/redis-index/actions?query=workflow:Build)\n[![codecov](https://codecov.io/gh/ErhoSen/redis-index/branch/master/graph/badge.svg)](https://codecov.io/gh/ErhoSen/redis-index)\n![License](https://img.shields.io/pypi/pyversions/redis-index.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI](https://img.shields.io/github/license/erhosen/redis-index.svg)](https://pypi.org/project/redis-index/)\n\n## Introduction\n\nSuppose you have to implement a service that will fetch data for a given set of filters.\n\n```http\nGET /api/companies?region=US&currency=USD&search_ids=233,816,266,...\n```\n\nFilters may require a significant costs for the database: each of them involves joining multiple tables. By writing a solution on raw SQL, we have a risk of stumbling into database performance.\n\nSuch "heavy" queries can be precalculated, and put into redis SET.\nWe can intersect the resulting SETs with each other, thereby greatly simplifying our SQL.\n\n```python\nsearch_ids = {233, 816, 266, ...}\nus_companies_ids = {266, 112, 643, ...}\nusd_companies_ids = {816, 54, 8395, ...}\n\nfiltered_ids = search_ids & us_companies_ids & usd_companies_ids  # intersection\n...\n"SELECT * from companies whrere id in {filtered_ids}"\n```\n\nBut getting such precalculated SETS from Redis to Python memory could be another bottleneck:\nfilters can be really large, and we don\'t want to transfer a lot of data between servers.\n\nThe solution is intersect these SETs directly in redis.\nThis is exactly what redis-index library does.\n\n## Installation\n\nUse `pip` to install `redis-index`.\n\n```bash\npip install redis-index\n```\n\n## Usage\n\n1) Declare your filters. They must inherit BaseFilter class.\n\n```python\nfrom redis_index import BaseFilter\n\nclass RegionFilter(BaseFilter):\n\n    def get_ids(self, region, **kwargs) -> List[int]:\n        """\n        get_ids should return a precalculated list of ints.\n        """\n        with psycopg2.connect(...) as conn:\n            with conn.cursor() as cursor:\n                cursor.execute(\'SELECT id FROM companies WREHE region = %s\', (region, ))\n                return cursor.fetchall()\n\nclass CurrencyFilter(BaseFilter):\n\n    def get_ids(self, currency, **kwargs):\n        with psycopg2.connect(...) as conn:\n            with conn.cursor() as cursor:\n                cursor.execute(\'SELECT id FROM companies WREHE currency = %s\', (currency, ))\n                return cursor.fetchall()\n```\n\n2) Initialize Filtering object\n\n```python\nfrom redis_index import RedisFiltering\nfrom hot_redis import HotClient\n\nredis_clent = HotClient(host="localhost", port=6379)\nfiltering = RedisFiltering(redis_clent)\n```\n\n3) Now you can use `filtering` as a singleton in your project.\nSimply call `filter()` method with specific filters, and your `search_ids`\n\n```python\ncompany_ids = request.GET["company_ids"]  # input list\nresult = filtering.filter(search_ids, [RegionFilter("US"), CurrencyFilter("USD")])\n```\n\nThe result will be a list, that contains only ids, that are both satisfying RegionFilter and CurrencyFilter.\n\n## How to warm the cache?\n\nYou can warm up the cache in various ways, for example, using the cron command\n```crontab\n*/5  *   *   *   *   python warm_filters\n```\n\nInside such a command, you can use specific method `warm_filters`\n\n```python\nresult = filtering.filter(search_ids, [RegionFilter("US"), CurrencyFilter("USD")])\n```\n\nOr directly RedisIndex class\n```python\nfor _filter in [RegionFilter("US"), CurrencyFilter("USD")]:\n    filter_index = RedisIndex(_filter, redis_client)\n    filter_index.warm()\n```\n\n## Statsd integration\n\nRedis-index optionally supports statsd-integration.\n\n![Redis-Index performance](https://github.com/ErhoSen/redis-index/raw/master/images/redis_index_performance.png "Redis-Index performance")\n\n![Redis-Index by filters](https://github.com/ErhoSen/redis-index/raw/master/images/redis_index_by_filters.png "Redis-Index by filters")\n\n## Code of Conduct\n\nEveryone interacting in the project\'s codebases, issue trackers, chat rooms, and mailing lists is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).\n\n## History\n\n### [0.1.11] - 2019-11-08\n\n#### Added\n\n- Added code for initial release\n',
    'author': 'Vladimir Vyazovetskov',
    'author_email': 'erhosen@gmail.com',
    'url': 'https://github.com/ErhoSen/redis-index',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
