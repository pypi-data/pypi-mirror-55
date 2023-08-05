from setuptools import setup
with open('README.md') as f:
    long_description = f.read()
setup(name='remember_forever',
      version='0.2',
      description='weixiao & yandong love story',
      long_description = long_description,
      packages=['remember_forever'],
      zip_safe=False)