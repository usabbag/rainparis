"""
Setup script for Rain Paris CLI tool
"""
from setuptools import setup, find_packages

setup(
    name='rainparis',
    version='1.0.0',
    description='Minute-by-minute rain forecasts for Paris arrondissements',
    author='Your Name',
    url='https://github.com/yourusername/rainparis',
    py_modules=['arrondissements'],
    scripts=['rainparis'],
    install_requires=[
        'requests>=2.31.0',
        'python-dotenv>=1.0.0',
    ],
    python_requires='>=3.7',
)
