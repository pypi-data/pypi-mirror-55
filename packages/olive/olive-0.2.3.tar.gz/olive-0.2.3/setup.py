import setuptools

setuptools.setup(name='olive',
                 version='0.2.3',
                 description='a python wrapper for an AIS Database API',
                 install_requires=[
                     'requests',
                     'requests_aws4auth',
                     'boto3',
                     'botocore'
                 ],
                 url='https://github.com/GeoBigData/AISDatabase',
                 author='Elizabeth Golden, Rachel Wegener, Melissa Dozier',
                 author_email='elizabeth.golden@digitalglobe.com',
                 license='',
                 packages=setuptools.find_packages(),
                 python_requires='>=3')


# up the version
# python3 setup.py sdist bdist_wheel
# delete old build files
# python3 -m twine upload dist/*
