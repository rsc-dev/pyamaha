from setuptools import setup
setup(
  name = 'pyamaha',
  packages = ['pyamaha'],
  version = '0.3',
  description = 'Python implementation of Yamaha Extended Control API Specification.',
  author = 'Radoslaw Matusiak',
  author_email = 'radoslaw.matusiak@gmail.com',
  url = 'https://github.com/rsc-dev/pyamaha',
  download_url = 'https://github.com/rsc-dev/pyamaha/releases/tag/0.3',
  keywords = ['Yamaha', 'API', 'Yamaha Extended Control'],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  install_requires=[
    'requests',
  ],
  setup_requires=["pytest-runner"],
  tests_require=["pytest"],
)