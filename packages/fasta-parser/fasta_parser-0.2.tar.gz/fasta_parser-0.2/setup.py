from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='fasta_parser',
      version='0.2',
      description='A first try on FASTA files parsing',
      classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        ],
      keywords='FASTA files parser',
      url='https://github.com/Fercho120/FASTA',
      author='Fernando Garcia',
      author_email='dfgr0316@gmail.com',
      license='MIT',
      packages=['fasta_parser'],
      include_package_data=True,
      install_requires=['Bio'],
      )
