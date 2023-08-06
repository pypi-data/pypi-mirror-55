import setuptools

# with open('requirements.txt', encoding='utf-8') as f:
#     requirements = f.read().split('\n')
#
# print(requirements)

setuptools.setup(name='olive',
                 version='0.2.1',
                 description='a python wrapper for an AIS Database API',
                 install_requires=[
                     'requests',
                     'requests_aws4auth',
                     'configparser'
                 ],
                 url='https://github.com/GeoBigData/AISDatabase',
                 author='Elizabeth Golden, Rachel Wegener, Melissa Dozier',
                 author_email='elizabeth.golden@digitalglobe.com',
                 license='',
                 packages=setuptools.find_packages(),
                 python_requires='>=3.6')


# python3 setup.py sdist bdist_wheel

# python3 -m twine upload dist/*
