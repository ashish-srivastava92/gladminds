from setuptools import setup, find_packages

setup(
    name="my_custom_project",
    version="0.0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['setuptools', 'Django'],
)
