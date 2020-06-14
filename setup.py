import setuptools
from trackpack.version import __version__

def long_description_readme():
    with open("README.md", "r") as readme_file:
        return readme_file.read()


setuptools.setup(
    name='trackpack',
    version=__version__,
    author='offa',
    author_email='offa@github',
    description='Package audio tracks.',
    long_description=long_description_readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/offa/trackpack',
    packages=['trackpack'],
    entry_points={"console_scripts": ["trackpack = trackpack.__main__:main"]},
    keywords=['audio', 'packaging', 'stems'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities',
    ],
    install_requires=['PyYAML']
)
