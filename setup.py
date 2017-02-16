import sys

from setuptools import find_packages, setup

assert sys.version_info >= (3, 3), "python >= 3.3 required"


# with open('requirements.txt') as requirements:
#     requires = requirements.read().splitlines()

requires = [
    'arrow',
    'pycommon>=0.5',
    'numpy'
]

setup(name='stockjournal',
      version="1.0",
      description='stock calculator',
      author='Robert Zaremba',
      author_email='robert.zaremba@scale-it.pl',
      packages=find_packages(exclude=['test', 'test.*', 'build.*']),
      install_requires=requires,
      tests_require=['pytest'],
      dependency_links=['git+https://github.com/robert-zaremba/py-common.git#egg=pycommon-0.5'],
      entry_points={
          'console_scripts': [
              # 'name = pkg.path:main',
          ]},
      classifiers=[
          'Environment :: Console',
          'Operating System :: OS Independent',

          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3 :: Only'])
