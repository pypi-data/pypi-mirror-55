from setuptools import find_packages, setup


PKG_NAME = 'list-cli'
PKG_DESCRIPTION = 'List Management Application (CLI)'
PKG_VERSION = open('VERSION'.format(PKG_NAME), 'r').read().rstrip()


setup(
    name=PKG_NAME,
    version=PKG_VERSION,
    url='https://github.com/jzaleski/list-cli',
    license='MIT',
    description=PKG_DESCRIPTION,
    long_description=PKG_DESCRIPTION,
    author='Jonathan W. Zaleski',
    author_email='JonathanZaleski@gmail.com',
    packages=find_packages(),
    install_requires=[],
    entry_points={'console_scripts': ['list-cli=list.__main__:main']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development',
    ],
    keywords=[
        'list',
        'list-cli',
        'task'
        'todo',
    ],
)
