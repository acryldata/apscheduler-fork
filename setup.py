import os.path

from setuptools import find_packages, setup

here = os.path.dirname(__file__)
readme_path = os.path.join(here, 'README.rst')
readme = open(readme_path).read()

setup(
    name='APScheduler',
    use_scm_version={
        'version_scheme': 'post-release',
        'local_scheme': 'dirty-tag'
    },
    description='In-process task scheduler with Cron-like capabilities',
    long_description=readme,
    author=u'Alex Grönholm',
    author_email='apscheduler@nextday.fi',
    url='https://github.com/agronholm/apscheduler',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
        'Programming Language :: Python :: 3.12'
        'Programming Language :: Python :: 3.13'
    ],
    keywords='scheduling cron',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.8',
    setup_requires=[
        'setuptools_scm'
    ],
    install_requires=[
        'pytz',
        'tzlocal >= 2.0, != 3.*',
    ],
    extras_require={
        'gevent': ['gevent'],
        'mongodb': ['pymongo >= 3.0'],
        'redis': ['redis >= 3.0'],
        'rethinkdb': ['rethinkdb >= 2.4.0'],
        'sqlalchemy': ['sqlalchemy >= 1.4'],
        'tornado': ['tornado >= 4.3'],
        'twisted': ['twisted'],
        'zookeeper': ['kazoo'],
        'etcd': ['etcd3', 'protobuf <= 3.21.0'],
        'test': [
            'pytest',
            'pytest_asyncio',
            'pytest-cov',
            'pytest-tornado5',
            'PySide6; python_implementation == "CPython"',
            'APScheduler[gevent,mongodb,redis,rethinkdb,sqlalchemy,tornado,twisted,zookeeper,etcd]'
        ],
        'doc': [
            'sphinx',
            'sphinx-rtd-theme',
            'APScheduler[gevent,mongodb,redis,rethinkdb,sqlalchemy,tornado,twisted,zookeeper,etcd]',
        ],
    },
    zip_safe=False,
    entry_points={
        'apscheduler.triggers': [
            'date = apscheduler.triggers.date:DateTrigger',
            'interval = apscheduler.triggers.interval:IntervalTrigger',
            'cron = apscheduler.triggers.cron:CronTrigger',
            'and = apscheduler.triggers.combining:AndTrigger',
            'or = apscheduler.triggers.combining:OrTrigger'
        ],
        'apscheduler.executors': [
            'debug = apscheduler.executors.debug:DebugExecutor',
            'threadpool = apscheduler.executors.pool:ThreadPoolExecutor',
            'processpool = apscheduler.executors.pool:ProcessPoolExecutor',
            'asyncio = apscheduler.executors.asyncio:AsyncIOExecutor [asyncio]',
            'gevent = apscheduler.executors.gevent:GeventExecutor [gevent]',
            'tornado = apscheduler.executors.tornado:TornadoExecutor [tornado]',
            'twisted = apscheduler.executors.twisted:TwistedExecutor [twisted]'
        ],
        'apscheduler.jobstores': [
            'memory = apscheduler.jobstores.memory:MemoryJobStore',
            'sqlalchemy = apscheduler.jobstores.sqlalchemy:SQLAlchemyJobStore [sqlalchemy]',
            'mongodb = apscheduler.jobstores.mongodb:MongoDBJobStore [mongodb]',
            'rethinkdb = apscheduler.jobstores.rethinkdb:RethinkDBJobStore [rethinkdb]',
            'redis = apscheduler.jobstores.redis:RedisJobStore [redis]',
            'zookeeper = apscheduler.jobstores.zookeeper:ZooKeeperJobStore [zookeeper]',
            'etcd = apscheduler.jobstores.etcd:EtcdJobStore [etcd]'
        ]
    }
)
