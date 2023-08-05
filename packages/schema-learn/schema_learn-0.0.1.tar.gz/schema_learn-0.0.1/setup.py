from setuptools import setup

setup(name='schema_learn',
      version='0.0.1',
      description='Framework for integrating heterogeneous modalities of data',
      url='http://github.com/rs239/schema',
      author='Rohit Singh',
      author_email='rsingh@alum.mit.edu',
      license='MIT',
      packages=['schema'],
      install_requires = 'numpy,scipy,pandas,sklearn,cvxopt'.split(','),
      zip_safe=False)
