from setuptools import setup

with open('readme.md') as f:
    long_description = f.read()

setup(name='chronologicon',
      version='5.5',
      description='A minimal time tracker',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/rutherfordcraze/chronologicon',
      author='Rutherford Craze',
      author_email='rutherford@craze.co.uk',
      license='MIT',
      packages=['chronologicon'],
      scripts=['bin/chron'],
      install_requires=['EasySettings'],
      include_package_data=True,
      zip_safe=False)
