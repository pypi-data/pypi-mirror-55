from setuptools import setup

setup(name='wx2pdf',
      version='1.0',
      description='A command line util to save article from wechat media platform',
      author='Chao Guo',
      author_email='jeffguorg@gmail.com',
      url='https://github.com/jeffguorg/wx2pdf',
      scripts=["wx2pdf.py"],
      long_description=open("README.md").read(),
      install_requires=list(filter(lambda x: x, map(lambda x: x.strip(), open("requirements.txt"))))
      )
