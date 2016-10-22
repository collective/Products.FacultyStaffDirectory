# Before releasing, make sure to update the translations:
# $ for po in `find . -name "*.po"` ; do msgfmt -o `dirname $po`/`basename $po .po`.mo $po; done
# # To build locally: python setup.py egg_info -RDb "" bdist_egg 
# To release: python setup.py egg_info -RD sdist bdist_egg register upload
# To create a named release: python setup.py egg_info -RDb "a1" sdist bdist_egg register upload
# To release a dev build: python setup.py egg_info -rD sdist bdist_egg register upload
# See http://peak.telecommunity.com/DevCenter/setuptools#release-tagging-options for more information.

from setuptools import setup, find_packages
import os

version = '5.0'

setup(name='Products.FacultyStaffDirectory',
      version=version,
      description="Provides content types for creating and organizing personnel directories within educational institutions. Integrates with Plone's users and groups infrastructure and supports an extensibility framework for custom requirements.",
      long_description=open("README.rst").read() + "\n\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)"
      ],
      keywords='',
      author='originally by WebLion Group, The Pennsylvania State University',
      author_email='',
      url='https://github.com/collective/Products.FacultyStaffDirectory',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Plone>=4.0',
          'Products.ATContentTypes',
          'archetypes.schemaextender',
          'Products.Relations>=0.9b1',
          'Products.membrane>=2.1.4',
          'archetypes.referencebrowserwidget'
      ],
      extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot]',
        ],
      },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
