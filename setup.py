from pip.req import parse_requirements
from setuptools import setup
import uuid

setup(
        name='json2csv',
        version='0.1',
        modules=['json2csv', 'endpoint2csv'],
        scripts=['json2csv.py'],
        url='https://github.com/evidens/json2csv',
        license='MIT License',
        author='evidens',
        author_email='',
        description='Converts JSON files to CSV (pulling data from nested structures). Useful for Mongo data',
        install_requires= ['unicodecsv==0.9.0']
)
