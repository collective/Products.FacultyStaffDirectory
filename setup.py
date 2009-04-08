# To build locally: python setup.py egg_info -RDb "" bdist_egg 
# To release: python setup.py egg_info -RD sdist bdist_egg register upload
# To create a named release: python setup.py egg_info -RDb "a1" sdist bdist_egg register upload
# To release a dev build: python setup.py egg_info -rD sdist bdist_egg register upload
# See http://peak.telecommunity.com/DevCenter/setuptools#release-tagging-options for more information.

from setuptools import setup, find_packages
import os

version = '2.1.1.2'

setup(name='Products.FacultyStaffDirectory',
      version=version,
      description="Provides content types for creating and organizing personnel directories within educational institutions. Integrates with Plone's users and groups infrastructure and supports an extensibility framework for custom requirements.",
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
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'archetypes.schemaextender<2.0',
          'Products.Relations==0.8.1',
          'Products.membrane>=1.1b1,<=1.1',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )