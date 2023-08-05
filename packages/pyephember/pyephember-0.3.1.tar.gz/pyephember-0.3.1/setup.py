from setuptools import setup, find_packages

setup(name='pyephember',
      version='0.3.1',
      description='Python library to work with ember from EPH Controls',
      keywords='eph ember',
      author='Thom Troy',
      author_email='ttroy50@gmail.com',
      license='MIT',
      url='https://github.com/ttroy50/pyephember',
      download_url='https://github.com/ttroy50/pyephember/archive/0.3.1.tar.gz',
      platforms=["any"],
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          'requests',
      ],
      test_requires=[
          'tox',
          'flake8',
          'pylint'
      ]
     )
