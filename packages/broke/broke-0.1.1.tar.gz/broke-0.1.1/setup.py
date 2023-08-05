from __future__ import absolute_import
from setuptools import setup
from setuptools import find_packages

setup(name='broke',
      version='0.1.1',
      description='Broke: Smooth broken link checker for git repositories',
      long_description='Broke: Smooth broken link checker for git repositories',
      url='http://github.com/KonduitAI/broke',
      download_url='https://github.com/KonduitAI/broke/tarball/0.1.1',
      author='Max Pumperla',
      author_email='max.pumperla@googlemail.com',
      install_requires=['requests', 'click'],
      entry_points={
        'console_scripts': [
            'broke=broke.cli:run'
        ]
      },
      packages=find_packages(),
      license='MIT',
      zip_safe=False,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ])
