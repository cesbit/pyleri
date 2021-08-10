"""setup.py

Upload to PyPI, Thx to: http://peterdowns.com/posts/first-time-with-pypi.html

python3 setup.py sdist
twine upload --repository pypitest dist/pyleri-x.x.x.tar.gz
twine upload --repository pypi dist/pyleri-x.x.x.tar.gz
"""
from setuptools import setup
from pyleri import __version__ as version

try:
    with open('README.md', 'r') as f:
        long_description = f.read()
except IOError:
    long_description = ''

setup(
    name='pyleri',
    packages=['pyleri'],
    version=version,
    description='Python Left-Right Parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jeroen van der Heijden',
    author_email='jeroen@cesbit.com',
    url='https://github.com/transceptor-technology/pyleri',
    download_url=(
        'https://github.com/transceptor-technology/'
        'pyleri/tarball/{}'.format(version)),
    keywords=['parser', 'grammar', 'autocompletion'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic'
    ],
)
