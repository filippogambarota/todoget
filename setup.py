from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='todoget',
    version='0.1.0',
    description='Extracting custom tags from a project',
    author='Filippo Gambarota',
    author_email='filippo.gambarota@gmail.com',
    long_description=long_description,
    packages=find_packages(),
    url='https://github.com/filippogambarota/todoget',
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    project_urls = {
        'Bug Tracker': 'https://github.com/filippogambarota/todoget/issues'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'todoget = todoget.cmd.cmd:todoget',
        ],
    },
)
