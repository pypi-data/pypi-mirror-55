from setuptools import setup
import sys,os
from os import path
import git

repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name = 'guiscrcpy',
    version = repo.git.describe("--tags")[:-9],
    description = 'An Open Source - Fast -  Android Screen Mirroring system.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPL v3',
    author = 'srevinsaju',
    author_email="srevin03@gmail.com",
    packages = ['guiscrcpy'],
    url = "https://srevinsaju.github.io/guiscrcpy",
    download_url = "https://github.com/srevinsaju/guiscrcpy/archive/master.zip",
    package_data={'guiscrcpy': ['*', '*.*', 'dark/*', 'icons/*', 'fonts/*', 'rsrc/*', 'ui/*'],
        '.':[".git/info/*"]
                 },
    include_package_data = True,
    install_requires=['PyQt5','psutil','qdarkstyle'],
    entry_points = {
        'console_scripts': [
            'guiscrcpy=guiscrcpy.__main__:launch_main']
            },
    #scripts = ["guiscrcpy"],
    classifiers = ['Operating System :: OS Independent',
            
            'Programming Language :: Python :: 3.6',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
)
