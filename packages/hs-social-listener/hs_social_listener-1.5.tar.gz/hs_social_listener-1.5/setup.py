from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='hs_social_listener',
      version='1.5',
      description='A library to analyse conversations on social media',
      url='https://hearts-science.com',
      author='James Londal',
      license='GNU AFFERO GENERAL PUBLIC LICENSE',
      install_requires=[
         'twint',
         'pandas',
         'numpy',
         'nest_asyncio',
         'textblob'
      ],
      packages=['hs_social_listener'],
      zip_safe=False,
      include_package_data=True
)
