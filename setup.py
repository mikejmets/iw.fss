from setuptools import setup, find_packages

version = '3.0.0a1'

setup(name='iw.fss',
      version=version,
      description="FileSystemStorage (FSS) is an Archetypes storage for storing fields raw values on the file system. This storage is used to avoid unnecessary growth of the ZODB's FileStorage (Data.fs) when using a lot of large files",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Archetypes Filesystem Storage',
      author='Ingeniweb',
      author_email='support@ingeniweb.com',
      url='http://plone.org/products/filesystemstorage',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['iw'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
