from setuptools import setup, find_packages

# with open('readme/readme.md', 'r') as f:
#     desc = f.read()

# REF: https://packaging.python.org/tutorials/packaging-projects/

requires = [
    "bs4>=0.0.1",
    "pdfminer.six",
    "pdfplumber>=0.5.14",
    "pypinyin>=0.36.0",
    "requests>=2.22.0",
    "xlrd>=1.2.0",
    "xlwt>=1.3.0",
    "xlutils>=2.0.0",
    "XlsxWriter>=1.2.0",
]

setup(
    name='lk_utils',
    version='1.1.6',
    description='Easy used for data processing.',
    author='Likianta',
    author_email='likianta@foxmail.com',
    url='https://github.com/likianta',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    python_requires='>=3.8',
    license='MIT License',
)
