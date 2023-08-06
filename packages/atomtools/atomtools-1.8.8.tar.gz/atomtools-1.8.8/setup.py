# coding=utf-8

import os
from setuptools import setup, find_packages

def get_version():
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import atomtools
    return atomtools.__version__


if __name__ == '__main__':
    setup(
        name='atomtools',
        version=get_version(),
        description=(
            'basic atom tools collection'
        ),
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        author='Sky Zhang',
        author_email='sky.atomse@gmail.com',
        maintainer='Sky Zhang',
        maintainer_email='sky.atomse@gmail.com',
        license='MIT License',
        packages=find_packages(),
        platforms=["Linux", "Darwin"],
        url='https://github.com/atomse/atomtools',
        python_requires='>=3',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Operating System :: MacOS',
            'Operating System :: POSIX',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
        install_requires=open('requirements.txt').read().split(),
        entry_points={
            "console_scripts": [
                "atomtools=atomtools.cli:run_atomtools_cli",
            ],
        },
        extras_require={
            'docs': [
                'sphinx',
                'sphinxcontrib-programoutput',
                'sphinx_rtd_theme',
                'numpydoc',
            ],
            'tests': [
                'pytest>=4.0',
                'pytest-cov'
            ],
            'curate': [
                'graphviz'
            ],
        },
        include_package_data = True,
        zip_safe=False,
    )
