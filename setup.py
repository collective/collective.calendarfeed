from setuptools import setup, find_packages
import os

version = '2.2.3'

setup(name='collective.fullcalendarioview',
      version=version,
      description="Collective FullCalendar.io view",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Fullcalendario view,Google Calendar,Portlet,View',
      author='David Bain',
      author_email='pigeonflight@gmail.com',
      url='http://github.com/collective/collective.fullcalendarview/',
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
