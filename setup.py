from setuptools import setup, find_packages

setup(
        name='pytomacco',
        version='0.1.0',
        author='Ryan Campbell',
        author_email='campbellr@gmail.com',
        url='https://github.com/campbellr/pytomacco',
        license='GPL3+',
        description='Python client/server implementation of the card game Tomacco',
        long_description=open('README.rst', 'r').read(),
        packages=find_packages(),
        zip_safe=False,
        # TODO: fill in with client/server scripts..
        #entry_points={},
        # TODO: fill in with dependencies
        #install_requires=[],
    )
