# To build locally: python setup.py egg_info -RDb "" bdist_egg 
# To release: python setup.py egg_info -RDb "" sdist bdist_egg register upload

from setuptools import setup, find_packages
import os

version = '2.1-dev'

setup(name='Products.FacultyStaffDirectory',
      version=version,
      description="",
      long_description=open("src/Products/FacultyStaffDirectory/HISTORY.txt").read() + "\n\n" +
                       open("src/Products/FacultyStaffDirectory/README.txt").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='WebLion Group, Penn State University',
      author_email='support@weblion.psu.edu',
      url='https://weblion.psu.edu/svn/weblion/weblion/Products.FacultyStaffDirectory',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['Products'    ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'archetypes.schemaextender',
          'Products.Relations',
          'Products.membrane',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )