import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE/"README.md").read_text()

setup(
    name="ChainTranslator",
    packages=["ChainTranslator"],
    version="1.0.6",
    license="MIT",
    description="a package to mess up text via google translate",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Benjamin Hinchliff",
    author_email="benjamin.hinchliff@gmail.com",
    url="https://github.com/SuniTheFish/ChainTranslator",
    keywords=["google", "translator", "useless", "stupid", "random", "chain", "translator", "ChainTranslator"],
    install_requires=[
        'googletrans'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Text Processing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    entry_points={
        "console_scripts": [
            "chaintranslator=ChainTranslator.__main__:main"
        ]
    }
)