import os
from setuptools import setup
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
   README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dataton-2023-optilab',
    version='1.0a0',
    packages=find_packages(),

    download_url='',

    install_requires=[ 
                     'numpy',
                     'ortools==9.7.2996',
                     'pandas',
                     'seaborn',
                     'matplotlib',
                     'docopt',
                     'xlsxwriter'
    ],

    entry_points={'console_scripts': [
        'get_schedule=dataton2023_optilab.engine:main',
         'get_plot=dataton2023_optilab.utils.plot:main'
        ]
        },

    include_package_data=True,
    #license='MIT License',
    description="",
    zip_safe=False,

    long_description=README,
    long_description_content_type='text/markdown',

    python_requires='>=3.10',

)