from setuptools import setup, find_packages

setup(
    name="gladminds",
    version="0.0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['setuptools', 'Django', 'celery', 'MySQL-python', 'gunicorn', 'django-suit', 'django-tastypie', 'requests', 'redis', 'flower', 'django-celery', 'south'],
)
