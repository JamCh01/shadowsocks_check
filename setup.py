import codecs
from setuptools import setup, find_packages

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="shadowsocks_check",
    version="0.1",
    license='https://www.gnu.org/licenses/lgpl-3.0.en.html',
    description=
    "You can check your SS server status by this script. And it will be the most graceful way.",
    author='JamCh01',
    author_email='jamcplusplus@gmail.com',
    url='https://github.com/jamcplusplus/shadowsocks_check',
    packages=find_packages(),
    install_requires=['requests', 'psutil'],
    package_data={'shadowsocks_check': ['README.rst', 'LICENSE']},
    entry_points={
        'console_scripts': [
            'ss-check = shadowsocks_check:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: GNU LESSER GENERAL PUBLIC LICENSE',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: Check Shadowsocks status',
    ],
    long_description=long_description,
)
