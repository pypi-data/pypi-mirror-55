from setuptools import setup, find_packages

setup(name="MegaMess_client",
      version="0.8.2",
      description="Mega messenger client",
      author="Maria Afanaseva",
      author_email="mashenkachukina@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
