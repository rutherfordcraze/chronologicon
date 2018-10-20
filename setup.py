from setuptools import setup

setup(name='chronologicon',
      version='4.14',
      description='A minimal time tracker',
      url='https://github.com/rutherfordcraze/chronologicon',
      author='Rutherford Craze',
      author_email='rutherford@craze.co.uk',
      license='MIT',
      packages=['chronologicon'],
      scripts=['bin/chron'],
      include_package_data=True,
      zip_safe=False)