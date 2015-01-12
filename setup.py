from setuptools import setup, find_packages
import os

version = '2.2.3'

setup(name='collective.calendarfeed',
      version=version,
      description="Collective Calendarfeed (for Google)",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Fullcalendar.io view,Google Calendar,Portlet,View',
      author='David Bain',
      author_email='david@alteroo.com',
      url='http://github.com/collective/collective.calendarfeed/',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
         "setuptools",
         "collective.js.moment",
         "five.grok",
         "plone.app.registry",
         "requests",
    # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
