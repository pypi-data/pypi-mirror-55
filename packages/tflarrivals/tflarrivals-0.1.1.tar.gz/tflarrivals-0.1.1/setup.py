from distutils.core import setup

with open("README.md", "r") as f:
  long_description = f.read()

setup(
  name='tflarrivals', 
  packages=['tflarrivals'],
  version='0.1.1',
  license='MIT',
  description='Library to fetch arrival times from TfL Unified API',
  long_description=long_description,
  author='Giancarlo Grasso',
  author_email='ggrasso.dev@gmail.com',
  url='https://github.com/Giannie/tflarrivals',
  download_url='https://github.com/Giannie/tflarrivals/archive/tflarrivals-v_0-1-1.tar.gz',
  keywords=['tfl', 'transport', 'london'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)