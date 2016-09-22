from setuptools import setup, find_packages


setup(
    name='csiphash',
    version='0.0.1',

    description='A CFFI-based implementation of SipHash24',
    url='https://github.com/zacharyvoase/python-csiphash',

    author='Zachary Voase',
    author_email='zack@meat.io',
    license='UNLICENSE',

    packages=find_packages(exclude=['test']),

    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["csiphash_build.py:ffibuilder"],

    install_requires=["cffi>=1.0.0"],
)
