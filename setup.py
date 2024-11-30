from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open('CHANGELOG.md', 'r', encoding='utf-8') as cl:
    changelog = cl.read()

setup(
    name='gptize',
    version='0.5.0',
    url='https://github.com/aabee-tech/gptize',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pathspec==0.11.2',
        'pyperclip==1.9.0',
        'tiktoken==0.8.0',
    ],
    author='SvetlovTech',
    author_email='svetlovtech@aabee.tech',
    description='Gptize is a tool designed to concatenate the contents of project files for ChatGPT',
    long_description=long_description + '\n\n' + changelog,
    long_description_content_type='text/markdown',
    python_requires='>=3.9.0',
    entry_points={
        'console_scripts': [
            'gptize=src.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
