import codecs
from setuptools import setup, find_packages

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="shadowsocks_check",
    version="0.2",
    license='https://www.gnu.org/licenses/lgpl-3.0.en.html',
    description=
    "You can check your SS server status by this script. And it will be the most graceful way.",
    author='JamCh01',
    author_email='me@jamchoi.cc',
    url='https://github.com/JamCh01/shadowsocks_check',
    packages=find_packages(),
    install_requires=['requests', 'psutil'],
    package_data={'shadowsocks_check': ['README.rst', 'LICENSE']},
    entry_points={
        'console_scripts': [
            'ss-check = shadowsocks_check:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Other/Nonlisted Topic',
    ],
    long_description=long_description,
)
