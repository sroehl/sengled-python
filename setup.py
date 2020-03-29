from distutils.core import setup
setup(
  name = 'SengledElement',
  packages = ['SengledElement'],
  version = '0.1',
  license='MIT',
  description = 'Library to control Sengled Element lights',
  author = 'Steven Roehl',
  author_email = 'stevenroehl@gmail.com',
  url = 'https://github.com/sroehl/sengled-python',
  download_url = 'https://github.com/sroehl/sengled-python/archive/0.1.tar.gz',
  keywords = ['sengled', 'element', 'lights'],
  install_requires=[
          'requests'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)