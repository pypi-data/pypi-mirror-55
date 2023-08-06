from setuptools import setup, find_packages

setup(
    name='sanic_macrobase',
    version='1.0.1',
    packages=find_packages(),
    url='https://github.com/mbcores/sanic-macrobase',
    license='MIT',
    author='Alexey Shagaleev',
    author_email='alexey.shagaleev@yandex.ru',
    description='Sanic driver for macrobase framework',
    install_requires=[
        'macrobase-driver>=1.0.0,<2.0.0',
        'sanic==18.12.0',
        'structlog==19.2.0'
    ]
)
