# -*- coding: utf-8 -*

import setuptools
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open(path.join(here, 'mavis', '__info__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

setuptools.setup(
    name='mix-mavis',
    version=about['__version__'],
    description='MAVIS 数据分析工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mixlinker/mavis',
    author=about['__author__'],
    author_email=about['__author_email__'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='visualization, analysis, jupyter',
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'IPython',
        'matplotlib',
        'seaborn',
        'ipywidgets',
        'numpy',
        'pandas',
        'scipy',
        'scikit-learn',
        'torch',
        'torchvision',
        'boto3'
    ])
