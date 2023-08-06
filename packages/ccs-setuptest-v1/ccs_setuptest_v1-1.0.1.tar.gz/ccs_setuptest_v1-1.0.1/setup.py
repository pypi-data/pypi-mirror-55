from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ccs_setuptest_v1',
    version='1.0.1',
    url='https://c-c-s.sourceforge.io/',
    author='Florian Strahberger',
    author_email='flori@ctemplar.com',
    description='a try to make the setuptest for the CYBR CSCW-SUITE (CCS) available - so, after your docker-compose --build up  you simply run this setuptest for setting up and test your just deployed CCS on your own server - via setting-up with the IP or localhost, setting-up the application-admin, the email-provider and so on - and install it with these values and run a show-up-test to show how it works and that it works',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="CYBR CSCW-SUITE,CCS,digital workplace,project management,digitalization,communication,collaboration,groupware, setup.install,test,selenium,pytest,chromedriver,setuptest",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    install_requires=['atomicwrites==1.3.0', 'attrs==19.3.0', 'importlib-metadata==0.23', 'more-itertools==7.2.0', 'packaging==19.2', 'pluggy==0.13.0', 'py==1.8.0', 'pyparsing==2.4.2', 'pytest==5.2.2', 'selenium==3.141.0', 'six==1.12.0', 'urllib3==1.25.6', 'wcwidth==0.1.7', 'zipp==0.6.0'],
)
