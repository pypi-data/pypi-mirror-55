#!/usr/bin/env python2.7

from setuptools import setup, find_packages

setup(
    name='openvpn_ipdb',
    version='1.0.0',
    description='Utility for managing OpenVPN IP address assignments',
    url='https://gitlab.com/MatthiasLohr/openvpn-ipdb',
    project_urls={
        'Bug Tracker': 'https://gitlab.com/MatthiasLohr/openvpn-ipdb/issues',
        'Source Code': 'https://gitlab.com/MatthiasLohr/openvpn-ipdb/tree/master'
    },
    author='Matthias Lohr',
    author_email='mail@mlohr.com',
    license='GPLv3',
    packages=find_packages(),
    python_requires='==2.7.*',
    install_requires=[
        'netaddr>=0.7.19'
    ],
    entry_points={
        'console_scripts': [
            'ipdb-client-connect=openvpn_ipdb.client_connect:main',
            'ipdb-client-disconnect=openvpn_ipdb.client_disconnect:main'
        ]
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Networking'
    ]
)
