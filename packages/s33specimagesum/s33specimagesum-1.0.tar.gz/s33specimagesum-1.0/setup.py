'''
 Copyright (c) 2019, UChicago Argonne, LLC
 See LICENSE file.
'''
from setuptools import setup, find_packages
import s33specimagesum

setup(name='s33specimagesum',
      version=s33specimagesum.__version__,
      description='Python Program to sum images in a scan.  This program was written'
      'for the case that each image in the scan ',
      author = 'John Hammonds, Christian Schleputz',
      author_email = 'JPHammonds@anl.gov',
      url = '',
      packages = find_packages() ,
      package_data = {'' : ['LICENSE',], },
      install_requires = ['spec2nexus',
                 'pillow',
                 'opencv',
                 'pyqt>5'
                 ],
      license = 'See LICENSE File',
      platforms = 'any',
      scripts = ['Scripts/s3specimagesum',
                 'Scripts/s33specimagesum.bat'],
      )