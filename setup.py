from setuptools import setup

setup(
    name='ExcelPostprocessor',
    version='0.1.0',
    packages=['excel_postprocessor'],
    package_dir={'': 'src'},
    url='https://github.com/DBMI/ExcelPostprocessor',
    license='',
    author='Kevin J. Delaney',
    author_email='kjdelaney@ucsd.edu',
    description='Python tools to search Excel columns and extract measurements.',
    entry_points={"console_scripts": ["excel_postprocessor=excel_postprocessor.__main__:main"]}
)
