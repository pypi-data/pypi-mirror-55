from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='literacy',
      version='0.1',
      url='https://github.com/holyfiddlex/literacy',
      author='Héctor de la Rosa Prado',
      author_email='hoftherose@gmail.com',
      description='Tools for literate programming in python and jupyter notebooks, following the functionality of Fastai v2 dev https://github.com/fastai/fastai_dev',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['literacy'],
      zip_safe=False)