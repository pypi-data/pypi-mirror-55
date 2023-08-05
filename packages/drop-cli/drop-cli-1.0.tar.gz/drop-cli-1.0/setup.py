from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='drop-cli',
    version='1.0',
    author='Maksim Bober',
    url="https://github.com/Bobrinik/drop",
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['drop'],
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'drop = drop:cli',
        ],
    },
    packages=find_packages(),
)
