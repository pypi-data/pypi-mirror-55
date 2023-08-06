import os

import setuptools
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='m-validator',
      version='0.1',
      description='Thư viện validate dữ liệu đầu vào',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='https://github.com/mobiovn',
      author='MOBIO',
      author_email='contact@mobio.vn',
      license='MIT',
      packages=['mobio/libs/validator'],
      package_data={'': '*.*'},
      install_requires=[],
      extras_require={
            'get_lang_from_request': ['flask']
      }
      )
