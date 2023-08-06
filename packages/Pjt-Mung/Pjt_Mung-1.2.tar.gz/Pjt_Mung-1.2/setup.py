from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name             = 'Pjt_Mung',
    version          = '1.2',
    description      = 'github-actions push deploy test',
    author           = 'JeongTae Park',
    author_email     = 'pjt3591oo@gmail.com',
    url              = 'https://github.com/pjt3591oo/pypi_github_actions_deploy',
    download_url     = '',
    install_requires = [], 
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages         = find_packages(exclude = ['docs', 'tests*']),
    keywords         = ['github', 'actions', 'deploy'],
    python_requires  = '>=3',
    package_data     =  {
        'pyquibase' : [
            'db-connectors/sqlite-jdbc-3.18.0.jar',
            'db-connectors/mysql-connector-java-5.1.42-bin.jar',
            'liquibase/liquibase.jar'
    ]},
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)