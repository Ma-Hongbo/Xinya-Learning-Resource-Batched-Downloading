from setuptools import setup

APP = ['main.py']
DATA_FILES = ['token.json']
OPTIONS = {
    'argv_emulation': False,
    'packages': ['requests'],
    'plist': {
        'CFBundleName': 'GitRepoDownloader',
        'CFBundleShortVersionString': '1.0',
        'CFBundleIdentifier': 'com.example.gitrepo',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
