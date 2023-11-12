from setuptools import setup, find_packages

setup(
    name='gptize',
    version='0.2.1',
    url='https://github.com/svetlovtech/gptize',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pathspec==0.11.2',
    ],
    author='Alexey Svetlov',
    python_requires='>=3.11.4',
    entry_points={
        'console_scripts': [
            'gptize=gptize.main:main',
        ],
    },
)
