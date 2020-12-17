from distutils.core import setup
setup(
  name = 'python_brightid',
  packages = ['brightid'],
  version = '1.1.2',
  license='MIT',
  description = 'SDK for integrating with BrightId!',
  author = 'Pooya Fekri',
  author_email = 'pooyafekri79@gmail.com',
  url = 'https://github.com/PooyaFekri/python-brightid',
  download_url = 'https://github.com/PooyaFekri/python-brightid/archive/main.zip',
  keywords = ['Brightid'],
  install_requires=[
          'requests',
          'ed25519',
          'pyqrcode',
          'pypng'
      ],
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.

    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.8'
  ],
)