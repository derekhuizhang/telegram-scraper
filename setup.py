from setuptools import setup

setup(
    name = 'telegram_scraper',
    version = '1.0.0',
    packages = ['scraper'],
    entry_points = {
        'console_scripts' : [
            'scraper = scraper.__main__:main'
        ]
    }
)
