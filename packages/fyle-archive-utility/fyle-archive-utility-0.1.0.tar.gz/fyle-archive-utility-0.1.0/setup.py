"""
Build the PyPi package.
"""

import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='fyle-archive-utility',
    version='0.1.0',
    author='Fyle',
    author_email='sravan.kumar@fyle.in',
    description='Command-line tool to download Fyle data.',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['fyle', 'data', 'archive', 'download', 'csv', 'json', 'python', 'sdk'],
    url='https://github.com/fylein/fyle-archive-utility',
    packages=setuptools.find_packages(),
    install_requires=[
        'logger==1.4'
        'Click==7.0'
        'fylesdk==0.10.0'
    ],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points='''
        [console_scripts]
        main=main:FyleArchive
    ''',
)
