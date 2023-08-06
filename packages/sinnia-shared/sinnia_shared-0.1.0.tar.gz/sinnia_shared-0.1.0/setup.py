from setuptools import setup, find_packages

setup(name='sinnia_shared',
      version='0.1.0',
      description='Sinnia Utilities',
      url='https://github.com/sinnia/scripts/tree/develop/shared',
      author='Sinnia',
      author_email='sonia.segura@sinnia.com',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
      install_requires=[
        'pymysql',
        'pyyaml'
      ],
      zip_safe=False)
