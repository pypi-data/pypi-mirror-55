from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='advanced_database_replace',
    version='1.0.0',
    packages=find_packages(exclude=('test', 'venv')),
    description=('Utility package which runs an advanced search&replace on a mysql database.'),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        'phpserialize>=1.3,<2.0',
        'PyMySQL>=0.9.3,<1.0.0',
    ],
    author='Laimonas Sutkus',
    author_email='laimonas.sutkus@gmail.com',
    keywords='Wordpress Database Replace Search Replace',
    url='https://github.com/laimonassutkus/AdvancedDatabaseReplace',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX :: Linux'
    ],
)
