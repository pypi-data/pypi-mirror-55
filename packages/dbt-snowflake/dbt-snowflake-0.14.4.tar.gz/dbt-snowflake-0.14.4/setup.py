#!/usr/bin/env python
from setuptools import find_packages
from distutils.core import setup
import os

package_name = "dbt-snowflake"
package_version = "0.14.4"
description = """The snowflake adapter plugin for dbt (data build tool)"""

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
    long_description_content_type='text/markdown',
    author="Fishtown Analytics",
    author_email="info@fishtownanalytics.com",
    url="https://github.com/fishtown-analytics/dbt",
    packages=find_packages(),
    package_data={
        'dbt': [
            'include/snowflake/dbt_project.yml',
            'include/snowflake/macros/*.sql',
            'include/snowflake/macros/**/*.sql',
        ]
    },
    install_requires=[
        'dbt-core=={}'.format(package_version),
        'snowflake-connector-python==2.0.3',
        'requests<2.23',
        'urllib3<1.25',
        'azure-common<2',
        'azure-storage-blob<3',
        'pycryptodomex>=3.2,!=3.5.0,<4',
        'pyOpenSSL>=16.2.0',
        'cffi>=1.9,<2',
        'cryptography>2,<3',
        'pyjwt<2',
        'idna<3',
        'ijson<2.6',
    ]
)
