from setuptools import setup, find_packages
import os

version = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Products', 'MobilePhoneExtender', 'version.txt')).read().strip()
if version.endswith('dev'):
    version = version[:-3]

setup(name='Products.MobilePhoneExtender',
      version=version,
      description="Adds a Mobile Phone field to FacultyStaffDirectory's Person objects",
      long_description="",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone zope facultystaffdirectory',
      author='WebLion',
      author_email='support@weblion.psu.edu',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'archetypes.schemaextender',
          'Products.FacultyStaffDirectory'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
