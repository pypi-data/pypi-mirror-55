from setuptools import setup

setup(name='django-handy-converters',
      version='2019.2',
      description='Some handy URL converters for django',
      packages=[
        'handy_converters'
      ],
      install_requires=[
        'django>=2.2.6',
      ],
      include_package_data=True,
      zip_safe=False)
