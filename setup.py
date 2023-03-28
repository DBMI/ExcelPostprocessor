from setuptools import setup

setup(
    name='ExcelPostprocessor',
    version='0.3.0',
    packages=['excelpostprocessor'],
    package_dir={'': 'src'},
    url='https://github.com/DBMI/ExcelPostprocessor',
    license='',
    author='Kevin J. Delaney',
    author_email='kjdelaney@ucsd.edu',
    description='Python tools to search Excel columns and extract measurements.',
    entry_points={"console_scripts": ["excelpostprocessor=excelpostprocessor.__main__:main"]}
)
