from setuptools import setup


setup(
   name='replica',
   version='1.0',
   description='A module for fine-tunning ChatGPT with personal chats',
   author='Valentina Feruere',
   author_email='valentinafeve@gmail.com',
   packages=['replica'],
   install_requires=['click'],
   entry_points={
      'console_scripts': [
         'replica=replica.cli:cli',
      ],
   },
)