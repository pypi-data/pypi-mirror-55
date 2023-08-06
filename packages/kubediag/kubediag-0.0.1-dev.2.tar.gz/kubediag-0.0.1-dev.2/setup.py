from distutils.core import setup
setup(
  name = 'kubediag',
  packages = ['kubediag'],
  version = '0.0.1-dev.2',
  license='MIT',
  description = 'Tool to diagnose common Kubernetes issues',
  author = 'Jason Forte',
  author_email = 'fortejas@amazon.com',
  url = 'https://github.com/fortejas/kubediag',
  download_url = 'https://github.com/fortejas/kubediag/archive/0.0.1.tar.gz',
  keywords = ['k8s', 'kubernetes', 'cli', 'troubleshooting'],
  scripts=['bin/kubediag'],
  install_requires=[
          'colorama',
          'kubernetes',
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)