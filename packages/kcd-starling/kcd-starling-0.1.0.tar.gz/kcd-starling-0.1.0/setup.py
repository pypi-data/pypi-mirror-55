from setuptools import setup, find_packages

setup(
    name='kcd-starling',
    version='0.1.0',
    description='Skeleton for Scrapper',
    author='Terry Cho',
    author_email='terry@kcd.co.kr',
    packages=find_packages(exclude=['test']),
    zip_safe=False
)