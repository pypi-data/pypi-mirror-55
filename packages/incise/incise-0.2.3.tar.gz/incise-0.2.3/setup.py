import setuptools
import itertools

with open('README.rst') as file:

    readme = file.read()

name = 'incise'

version = '0.2.3'

author = 'Exahilosys'

url = f'https://github.com/{author}/{name}'

extensions = {
    'events': [
        'wrapio',
        'lineopt'
    ]
}

setuptools.setup(
    name = name,
    version = version,
    url = url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    description = 'Live Segmentation Framework.',
    long_description = readme,
    extras_require = {
        'docs': [
            'sphinx',
            *set(itertools.chain.from_iterable(extensions.values()))
        ],
        **extensions
    }
)
