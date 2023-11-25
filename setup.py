from setuptools import setup, find_packages
import os

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open('CHANGELOG.md', 'r', encoding='utf-8') as cl:
    changelog = cl.read()

setup(
    name='gptize',
    version='0.2.5',
    url='https://github.com/svetlovtech/gptize',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pathspec==0.11.2',
    ],
    author='SvetlovTech',
    author_email='alexeysvetlov92@gmail.com',
    description='Gptize is a tool designed to concatenate the contents of project files for ChatGPT',
    long_description=long_description + '\n\n' + changelog,
    long_description_content_type='text/markdown',
    python_requires='>=3.9.0',
    entry_points={
        'console_scripts': [
            'gptize=gptize.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
