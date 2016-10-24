from distutils.core import setup

VERSION = '1.1.3'

setup(
    name='pyleri',
    packages=['pyleri'],
    version=VERSION,
    description='Python Left-Right Parser',
    author='Jeroen van der Heijden',
    author_email='jeroen@transceptor.technology',
    url='https://github.com/transceptor-technology/pyleri',
    download_url=
        'https://github.com/transceptor-technology/'
        'pyleri/tarball/{}'.format(VERSION),
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
