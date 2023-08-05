import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='wils',
    version='0.1.0',
    author='wbswjc',
    author_email='me@wbswjc.com',
    description='Utils used by wbswjc himself',
    long_description=long_description,
    url='https://github.com/wbswjc/wils',
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
)
