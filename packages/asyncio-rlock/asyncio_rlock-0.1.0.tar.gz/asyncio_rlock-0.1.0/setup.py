from setuptools import find_packages
from setuptools import setup

setup(
    name='asyncio_rlock',
    version='0.1.0',
    packages=find_packages(exclude=['tests', 'tests/**/*']),
    keywords="asyncio rlock",
    url='https://gitlab.com/heckad/asyncio_rlock',
    project_urls={'Source Code': 'https://gitlab.com/heckad/asyncio_rlock'},
    license='MIT',
    author='Heckad (Kazantcev Andrey)',
    author_email='heckad@yandex.ru',
    description='Rlock like in threading module but for asyncio.',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
