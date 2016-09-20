import os
from setuptools import setup, find_packages

version = '0.0.1.dev0'

setup(
    name='opensesame',
    version=version,
    description="Commandline-based password manager",
    long_description=open("README.rst").read() + "\n" +
                     open(os.path.join("CHANGES.rst")).read(),
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords='',
    author='JC Brand',
    author_email='jc@opkode.com',
    include_package_data=True,
    url='https://github.com/jcbrand/opensesame',
    license='GPLv3',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=[
        'setuptools',
        'python-gnupg',
        'python-awk',
        'clipboard',
        'pwgen',
        'ipdb'
    ],
    entry_points="""
    [console_scripts]
    opensesame = opensesame:main
    """,
)
