from setuptools import setup
import os

def _post_install(setup):
    def _post_actions():
        os.system("python -m textblob.download_corpora")
    _post_actions()
    return setup


_post_install(setup(name='hs_social_listener',
      version='1.7',
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
))
