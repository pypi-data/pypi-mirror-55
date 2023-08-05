from setuptools import setup

setup(name='PIcleaner',
      version='1.0',
      description='Clean the dirty things in our lovely data.',
      url='',
      author='Dung Le (Eric)',
      author_email='dung.le@pandoraintelligence.com',
      license='Pandora Intelligence',
      packages=['PIcleaner'],
      install_requires=[
          'clean-text[gpl]',
          'spacy',
      ],
      zip_safe=False)