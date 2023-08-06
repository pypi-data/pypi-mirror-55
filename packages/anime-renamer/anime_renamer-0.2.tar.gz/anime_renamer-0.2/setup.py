from setuptools import setup

setup(
    name='anime_renamer',
    version='0.2',
    packages=['anime_renamer'],
    entry_points={
        'console_scripts': [
            'anime_renamer = anime_renamer.__main__:main'
        ]
    },
    url='https://github.com/smsriharsha/anime-renamer',
    license='MIT',
    author='kudoark',
    author_email='',
    description='', install_requires=['requests', 'tvdbsimple']
)
